from azure import functions

import function_app


def test_plain_redirect():
    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
    )
    func = (
        function_app.redirect.build().get_user_function()
    )  # Gets through the wrappers
    resp = func(req)
    assert resp.status_code == "302"
    assert resp.headers["Location"] == "https://mas.to/@moof/109642947257051795"


def test_route():
    req = functions.HttpRequest(
        method="GET",
        url="http://localhost:7071/https://mas.to/@moof/109642947257051795",
        route_params={"destination": "https://mas.to/@moof/109642947257051795"},
        body=b"",
    )
    app = functions.AsgiFunctionApp(function_app.app)
    app.http_
