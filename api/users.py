from pysqlcipher3 import dbapi2 as sqlite
from flask import Flask, g, json, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import time

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = '../db/users.db'


# Function to connect to the database
def get_db():
    with open('../passphrases.json') as f:
        passphrases = json.load(f)
        secret_key = passphrases['users']['dbSecret']
        
    if 'db' not in g:
        g.db = sqlite.connect(DATABASE)
        g.db.execute("PRAGMA key=" + "'" + secret_key + "'" +  ";")
        g.db.execute("PRAGMA cipher_compatibility = 4;")
        g.db.row_factory = sqlite.Row
    return g.db


@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

# Teardown function to close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


#AUTHENTICATE USER
@app.route("/api/users/authenticate", methods=["POST"])
def authenticate():
    #REMOVE AFTER TESTING -START
    time.sleep(2)


    data = request.json
    print("data", data)

    decrypted_password = decrypt_password(data['password'])
    print("decrypted_password", decrypted_password)

    db = get_db()
    cursor = db.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Convert SQLite Row objects to dictionaries for JSON serialization
    result = []
    for row in rows:
        result.append(dict(row))
        for row in rows:
            if row['email'] == data['email'] and row['password'] == decrypted_password:
                return jsonify({'message': 'Authentication successful', 
                                'success': True, 
                                'data': {'firstName': row['first_name'], 
                                         'lastName': row['last_name'], 
                                         'email': row['email'], 
                                         'id': row['id']
                                         }
                                }
                            )
        return jsonify({'message': 'Authentication failed', 'success': False})

def decrypt_password(data):
    with open('../passphrases.json') as f:
        passphrases = json.load(f)
        secret_key = passphrases['users']['passwordEncryptionKey']
   
    secret_key = bytes(secret_key, 'utf-8')
    encrypted_message = base64.b64decode(data['encrypted_message'])

    iv = base64.b64decode(data['iv'])

    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode('utf-8')

    print("decrypted_message", decrypted_message)
    return decrypted_message


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)