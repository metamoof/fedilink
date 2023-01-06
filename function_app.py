import logging

import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="redirect")
@app.route(route="{*destination}")
async def redirect(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        status_code="302", headers={"Location": req.route_params["destination"]}
    )
