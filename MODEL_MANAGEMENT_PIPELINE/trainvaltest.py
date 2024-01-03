import requests


def train_test_val():
    print("SONO SU MODEL MANAGEMENT, ALLENO IL MODELLO")
    print("SALVO IL MODELLO")

  
    # Esempio di richiesta POST per salvare una stringa
    base_url = 'http://localhost:6070/save'

    data_to_save = {'data': 'SONO UN MODELLO!'}
    response = requests.post(base_url, json=data_to_save)

    # Verifica della risposta
    if response.status_code == 200:
        print('MODELLO salvato con successo!')
    else:
        print(f'Errore durante il salvataggio dei dati: {response.text}')

    
 
