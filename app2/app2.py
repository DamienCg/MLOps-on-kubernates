import requests
import json
from pathlib import Path
from datetime import datetime

url = "http://127.0.0.1:5000"

# Effettua la richiesta HTTP
response = requests.get(url)

# Ottieni l'oggetto datetime corrente
current_datetime = datetime.now()

# Formatta l'oggetto datetime come stringa
timestamp_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


if response.status_code == 200:

    # Stampa il nuovo dato
    print(f"Recupero dati: {response.text}"+f" - Timestamp attuale: {timestamp_str}")

    import requests

    # URL dell'applicazione Flask in esecuzione
    base_url = 'http://localhost:4949'

    # API per scrivere
    write_api_url = f'{base_url}/api/write'

    # API per leggere
    read_api_url = f'{base_url}/api/read'

    # Scrivi qualcosa chiamando l'API /api/write
    content_to_write = 'Hello, Flask!'
    write_data = {'content': content_to_write}
    response = requests.post(write_api_url, json=write_data)

    if response.status_code == 201:
        item_id = response.json().get('id')
        print('Scrittura riuscita!')

        # Leggi 
        read_api_url_with_id = f'{read_api_url}/{item_id}'
        response = requests.get(read_api_url_with_id)
        if response.status_code == 200:
            content_read = response.json().get('content')
            print(f'Contenuto letto: {content_read}')
        else:
            print(f'Errore durante la lettura: {response.status_code} - {response.json()}')
    else:
        print(f'Errore durante la scrittura: {response.status_code} - {response.json()}')

else:
    print(f"Error in the request: {response.status_code}")
