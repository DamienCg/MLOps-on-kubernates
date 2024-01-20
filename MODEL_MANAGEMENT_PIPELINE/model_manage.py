import requests
from trainvaltest import train_test_val

# URL del FEATURES_STORE
base_url = 'http://features_store:4949'

# API per leggere
read_api_url = f'{base_url}/api/read'

# Leggi 
item_id = 1

read_api_url_with_id = f'{read_api_url}/{item_id}'
response = requests.get(read_api_url_with_id)
if response.status_code == 200:
    content_read = response.json().get('content')
    print(f'La model management legge dal features store')
    checkpoint,precision = train_test_val(content_read)
    if checkpoint is not None:
        print("Salvo il checkpoint sul model store")
        endpoint_url = 'http://model_store:6070/save_checkpoint'

        files = {'checkpoint': checkpoint['checkpoint']}
        data = {'precision': str(precision)}

        # Invia la richiesta
        response = requests.post(endpoint_url, files=files, data=data)
        print(response.text) 
else:
    print(f'Errore durante la lettura: {response.status_code} - {response.json()}')



