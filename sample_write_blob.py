import logging

import azure.functions as func

def main(req: func.HttpRequest,outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = 'some_name'
    if not name:
        try:
            req_body = 'req_body_test'#req.get_json()
        except ValueError:
            pass
    else:
        name = 'name'#req_body.get('name')
    
    print(str(req.get_json()))

    outputblob.set(str(req.get_json()))
