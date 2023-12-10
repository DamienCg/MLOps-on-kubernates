import requests



print("SONO SULLA WEBAPP")
print("CARICO IL MODELLO")

# Esempio di richiesta GET per ottenere l'ultima entry
get_last_entry_url = 'http://localhost:6070/get_last_entry'
    
response = requests.get(get_last_entry_url)

# Verifica della risposta
if response.status_code == 200:
    data = response.json()
    print(f'Ultimo MODELLO nel database: {data}')
else:
    print(f'Errore durante il recupero dei dati: {response.text}')

    
    