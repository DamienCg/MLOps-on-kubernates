from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Creazione del database e della tabella
conn = sqlite3.connect('local_db.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Endpoint per salvare una stringa nel database
@app.route('/save', methods=['POST'])
def save_to_db():
    data = request.json.get('data')

    if not data:
        return jsonify({'error': 'Il campo "data" è obbligatorio'}), 400

    conn = sqlite3.connect('local_db.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (data) VALUES (?)', (data,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Dati salvati correttamente'}), 200

# Endpoint per recuperare l'ultima entry salvata
@app.route('/get_last_entry', methods=['GET'])
def get_last_entry():
    conn = sqlite3.connect('local_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()

    if result:
        entry_id, data = result
        return jsonify({'id': entry_id, 'data': data}), 200
    else:
        return jsonify({'message': 'Nessuna entry trovata'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6070)
