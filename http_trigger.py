import os
import json
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    if 'pages' in req_body and req_body['pages'][0]['title']:
        logging.info(req_body)
        return func.HttpResponse("Page is " + req_body['pages'][0]['title'] + ", Action is " + req_body['pages'][0]['action'])

    else:
        return func.HttpResponse("Invalid payload for Wiki event")
