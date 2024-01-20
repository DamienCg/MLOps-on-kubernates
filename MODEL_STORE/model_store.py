import os
from flask import Flask, Response, request, jsonify
import sqlite3
import time
import psutil
from inference import predict
from prometheus_flask_exporter import PrometheusMetrics
import json

app = Flask(__name__)
metrics = PrometheusMetrics(app)

conn = sqlite3.connect('local_db.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        checkpoint BLOB NOT NULL,
        time_stamp TIMESTAMP NOT NULL,
        precision FLOAT NOT NULL
    )
''')
conn.commit()
conn.close()


def refresh_value_matrics(Inference_time):
    # Nome del file JSON
    file_path = "./metric_inference.json"

    # Carica il contenuto del file JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Aggiorna i valori
    data["Inference_time"] = Inference_time

    # Risalva il file JSON sovrascrivendo il vecchio
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


@app.route('/save_checkpoint', methods=['POST'])
def save_checkpoint_to_db():
    checkpoint_file = request.files.get('checkpoint')
    precision = request.form.get('precision')

    # Validazione della precisione
    try:
        precision = float(precision)
    except ValueError:
        return jsonify({'error': 'Il campo "precision" non è un numero valido'}), 400

    if not checkpoint_file:
        return jsonify({'error': 'Il campo "checkpoint" è obbligatorio'}), 400

    # Cambiato il modo in cui viene costruito il nome del file di checkpoint
    time_stamp = time.strftime('%Y%m%d%H%M%S')
    checkpoint_filename = f'checkpoint_{time_stamp}_{precision}.ckpt'
    checkpoint_file.save(checkpoint_filename)

    with open(checkpoint_filename, 'rb') as f:
        checkpoint_data = f.read()

    conn = sqlite3.connect('local_db.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (checkpoint, time_stamp, precision) VALUES (?, ?, ?)',
                   (sqlite3.Binary(checkpoint_data), time_stamp, precision))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Checkpoint salvato correttamente'}), 200




@app.route('/get_predict', methods=['POST'])
def get_latest_checkpoint():
    data = request.json

    if not data:
        return jsonify({'error': 'Il corpo della richiesta deve contenere un oggetto JSON'}), 400

    conn = sqlite3.connect('local_db.db')
    cursor = conn.cursor()

    # Recupera l'ultima istanza del database ordinata per time_stamp
    cursor.execute('SELECT checkpoint FROM entries ORDER BY time_stamp DESC LIMIT 1')
    checkpoint = cursor.fetchone()
    checkpoint = checkpoint[0]
    
    # Calcolo del tempo impiegato per l'esecuzione dello script
    start_time = time.time()
    result = predict(data, checkpoint)
    end_time = time.time()
    inference_duration = end_time - start_time

    # Misura della memoria RAM utilizzata
    memory_used = psutil.Process(os.getpid()).memory_info().rss

    refresh_value_matrics(inference_duration)
   

    # TODO crea un dataload dal json sample ricevuto
    # dataloader from json (data) TODO DA FARE!
    return str(result)

@app.route('/metrics')
def metrics():

    file_path = "./metric_inference.json"

    # Carica il contenuto del file JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    view_metric = {'Inference_time':  data["Inference_time"]}

    metrics = ""
    for Inference_time in view_metric.items():
        metrics += 'Inference_details{metric="%s"} %s\n' % (Inference_time)

    return metrics

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6070)
