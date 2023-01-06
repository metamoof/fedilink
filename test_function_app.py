from typing import Any, Awaitable, Callable, Coroutine

import pytest
from azure import functions

import function_app


def unwrap_http_function(
    func,
) -> Callable[[functions.HttpRequest], Awaitable[functions.HttpResponse]]:
    return func.build().get_user_function()


@pytest.mark.asyncio
async def test_plain_redirect():
    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
        headers={
            "Cookie": "input_requests_remaining=0; HttpOnly; SameSite=Strict; Secure; Version=1"
        },
    )
    func = (
        function_app.redirect.build().get_user_function()
    )  # Gets through the wrappers
    resp = await func(req)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "https://mas.to/@moof/109642947257051795"


@pytest.mark.asyncio
async def test_instance_request_cookie():
    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
        headers={},
    )
    func = unwrap_http_function(function_app.redirect)  # Gets through the wrappers
    resp = await func(req)
    assert resp.status_code == 200
    assert (
        resp.headers["Set-Cookie"]
        == "input_requests_remaining=2; HttpOnly; Max-Age=5184000; SameSite=Strict; Secure; Version=1"
    )
    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
        headers={"Cookie": resp.headers["Set-Cookie"]},
    )
    resp = await func(req)
    assert resp.status_code == 200
    assert (
        resp.headers["Set-Cookie"]
        == "input_requests_remaining=1; HttpOnly; Max-Age=5184000; SameSite=Strict; Secure; Version=1"
    )

    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
        headers={
            "Cookie": "input_requests_remaining=1; HttpOnly; SameSite=Strict; Secure; Version=1; Max-Age=5183210"
        },
    )
    resp = await func(req)
    assert resp.status_code == 200
    assert (
        resp.headers["Set-Cookie"]
        == "input_requests_remaining=0; HttpOnly; Max-Age=5184000; SameSite=Strict; Secure; Version=1"
    )

    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
        headers={"Cookie": resp.headers["Set-Cookie"]},
    )
    resp = await func(req)
    assert resp.status_code == 302
    assert (
        resp.headers["Set-Cookie"]
        == "input_requests_remaining=0; HttpOnly; Max-Age=5184000; SameSite=Strict; Secure; Version=1"
    )
    assert resp.headers["Location"] == "https://mas.to/@moof/109642947257051795"
