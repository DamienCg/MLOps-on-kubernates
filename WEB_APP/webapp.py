import requests
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import time



# Carica il dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Dividi il dataset in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("SONO SULLA WEBAPP")
print("CARICO IL MODELLO")

json_dati_per_inferece = X_test[0].tolist()

# Esempio di richiesta GET per ottenere l'ultima entry
endpoint_url = 'http://model_store:6070/get_predict'

for _ in range(1000):

    response = requests.post(endpoint_url, json=json_dati_per_inferece)


    # Verifica della risposta
    if response.status_code == 200:
        data = response.json()
        print(f'PREVISIONE: {data}')
    else:
        print(f'Errore durante il recupero dei dati: {response.text}')

    # Metti in pausa per 5 secondi
    time.sleep(5)



    
    