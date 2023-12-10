import requests

# URL del FEATURES_STORE
base_url = 'http://localhost:4949'

# API per leggere
read_api_url = f'{base_url}/api/read'

# Leggi 
item_id = 1

read_api_url_with_id = f'{read_api_url}/{item_id}'
response = requests.get(read_api_url_with_id)
if response.status_code == 200:
    content_read = response.json().get('content')
    print(f'La model management legge dal features store: {content_read}')
else:
    print(f'Errore durante la lettura: {response.status_code} - {response.json()}')