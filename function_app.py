import logging
import os
import azure.functions as func
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def write_to_blob(data, blob_path, connection_string):
    container = os.environ.get("ContainerName")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_path)
    blob_client.upload_blob(data, overwrite=True)

@app.function_name(name="http_trigger")

@app.route(route="http_trigger")


def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    if 'pages' in req_body and req_body['pages'][0]['title']:
        # Obter data e hora atual
        now = datetime.now()

        # Extrair informações de data
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        
        # Extrair informações de hora
        hour = now.strftime('%H')
        minute = now.strftime('%M')
        second = now.strftime('%S')
        
        
        # Adiciona o registro ao final da lista
        #records.append(req_body)
        records = [req_body]  # Initialize records list with the current request body

        # Converte a lista de registros para JSON
        output_json = json.dumps(records)

        azure_webjobs_storage = os.environ.get("AzureWebJobsStorage")

        blob_path = "conversion_events/{}/{}/{}/Wiki-{}-{}-{}_{}:{}:{}.json".format(year, month, day, year, month, day, hour, minute, second)

        connection_string = azure_webjobs_storage

        write_to_blob(output_json, blob_path, connection_string)

        #return func.HttpResponse("Page is " + req_body['pages'][0]['title'] + ", Action is " + req_body['pages'][0]['action']),
        return func.HttpResponse(f"Evento capturado com sucesso e gravado em: {blob_path}")
    
    else:
        return func.HttpResponse("Invalid payload for Wiki event")
