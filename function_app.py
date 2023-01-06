import http.cookies
import logging
import os

import azure.functions as func

app = func.FunctionApp()


@app.function_name("home")
@app.route("home")
async def home(req: func.HttpRequest) -> func.HttpResponse:
    cookiestring = req.headers.get("Cookie", "")
    cookies = http.cookies.SimpleCookie(cookiestring)

    resp = func.HttpResponse(body=f"Home Page.\n{cookies.output()}")
    return resp


@app.function_name("cookies_delete")
@app.route("cookies/delete")
async def cookies_delete(req: func.HttpRequest) -> func.HttpResponse:
    cookiestring = req.headers.get("Cookie", "")
    cookies = http.cookies.SimpleCookie(cookiestring)

    resp = func.HttpResponse(status_code=302, headers={"Location": "/home"})

    for key in cookies:
        morsel = cookies[key]
        del morsel["max-age"]
        morsel["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
        morsel["path"] = "/"
        cookies[key] = None
        resp.headers.add("Set-Cookie", morsel.OutputString())
    return resp


@app.function_name(name="redirect")
@app.route(route="{*destination}")
async def redirect(req: func.HttpRequest) -> func.HttpResponse:
    cookiestring = req.headers.get("Cookie", "")
    cookies = http.cookies.SimpleCookie(cookiestring)
    if "destination" not in req.route_params:
        resp = func.HttpResponse(status_code=302, headers={"Location": "/home"})

    elif cookies.get("instance_url"):
        resp = func.HttpResponse(
            status_code=302, headers={"Location": req.route_params["destination"]}
        )
    elif (
        "input_requests_remaining" not in cookies
        or int(cookies["input_requests_remaining"].value) < 0
    ):
        cookies["input_requests_remaining"] = (
            int(os.environ.get("MaxInputRequests", "3")) - 1
        )

        resp = func.HttpResponse(
            body=f"Request an instance. Remaining: {cookies['input_requests_remaining'].value}"
        )
    elif int(cookies["input_requests_remaining"].value) > 0:
        cookies["input_requests_remaining"] = (
            int(cookies.get("input_requests_remaining").value) - 1
        )
        resp = func.HttpResponse(
            body=f"Request an instance. Remaining: {cookies['input_requests_remaining'].value}"
        )

    else:  # input_requests_remaining = 0
        resp = func.HttpResponse(
            status_code=302, headers={"Location": req.route_params["destination"]}
        )

    for morsel in cookies.values():
        morsel["max-age"] = os.environ.get("CookieMaxAge", 5184000)  # default: 60 days
        morsel["secure"] = True
        morsel["httponly"] = True
        morsel["samesite"] = "Strict"
        morsel["version"] = 1
        morsel["path"] = "/"
        resp.headers.add("Set-Cookie", morsel.OutputString())

    return resp
