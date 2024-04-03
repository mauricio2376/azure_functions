import logging
import azure.functions as func
import json
from datetime import datetime, timedelta


def get_blob_path():
    # Obter data e hora atual
    #now = datetime.now() + timedelta(days=3)  # Adicionando um dia
    now = datetime.now()

    # Extrair informações
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # Caminho para o blob
    path = f"fsbdntest/{year}/{month}/{day}/Wiki-{year}-{month}-{day}.json"
    
    return path

# Inicializa uma lista para armazenar os registros
records = []

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="http_trigger")

@app.route(route="http_trigger")

@app.blob_output(arg_name="outputblob",
                path=get_blob_path(),
                connection="AzureWebJobsStorage")



def http_trigger(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blob_service = "https://strfuncappbdn.blob.core.windows.net/"
    path=get_blob_path()

    req_body = req.get_json()

    if 'pages' in req_body and req_body['pages'][0]['title']:
        
        # Adiciona o registro ao final da lista
        records.append(req_body)

        # Converte a lista de registros para JSON
        output_json = json.dumps(records)

        # Grava o JSON de saída no blob
        outputblob.set(output_json)

        #return func.HttpResponse("Page is " + req_body['pages'][0]['title'] + ", Action is " + req_body['pages'][0]['action']),
        return func.HttpResponse(f"Evento capturado com sucesso e gravado em: {blob_service}{path}")
    
    else:
        return func.HttpResponse("Invalid payload for Wiki event")
    