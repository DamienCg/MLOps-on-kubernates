from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # Database SQLite locale
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

@app.route('/api/write', methods=['POST'])
def write_to_db():
    try:
        data = request.get_json()
        content = data.get('content')

        new_item = Item(content=content)
        db.session.add(new_item)
        db.session.commit()

        return jsonify({'id': new_item.id, 'message': 'scrittura sul FEATURES STORE avvenuta'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/read/<int:item_id>', methods=['GET'])
def read_from_db(item_id):
    try:
        item = Item.query.get(item_id)
        if item:
            return jsonify({'id': item.id, 'content': item.content})
        else:
            return jsonify({'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=4949)


