import logging
import azure.functions as func
import json
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def get_blob_path():
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    path = f"fsbdntest/{year}/{month}/{day}/Wiki-{year}-{month}-{day}.json"
    return path

def write_to_blob(data, blob_path, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container="container-name", blob=blob_path)
    blob_client.upload_blob(data, overwrite=True)

def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    if 'pages' in req_body and req_body['pages'][0]['title']:
        records = [req_body]  # Initialize records list with the current request body
        output_json = json.dumps(records)

        connection_string = "YOUR_CONNECTION_STRING"
        blob_path = get_blob_path()

        write_to_blob(output_json, blob_path, connection_string)

        return func.HttpResponse(f"Evento capturado com sucesso e gravado em: {blob_path}")
    else:
        return func.HttpResponse("Invalid payload for Wiki event")
