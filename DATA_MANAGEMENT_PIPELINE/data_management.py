import requests
import json
from pathlib import Path
from datetime import datetime
import requests

url = "http://localhost:5000"

response = requests.get(url)

print("DATA MANAGEMENT AVVIATA!")

if response.status_code == 200:

    print(f"La data management recupera dati dalla fonte esterna: {response.text}")

else:
    print(f"Error in the request: {response.status_code}")


# URL del FEATURES_STORE
base_url = 'http://localhost:4949'

# API per scrivere
write_api_url = f'{base_url}/api/write'

# API per leggere
read_api_url = f'{base_url}/api/read'

content_to_write = 'CIAOO!'
write_data = {'content': content_to_write}
response = requests.post(write_api_url, json=write_data)

if response.status_code == 201:
    item_id = response.json().get('id')
    print('La data management scrive: '+content_to_write+"sul features store")

else:
    print(f'Errore durante la scrittura: {response.status_code} - {response.json()}')

