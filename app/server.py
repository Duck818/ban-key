import os
from flask import Flask, jsonify, send_from_directory
import random
import string
import time

app = Flask(__name__)
active_keys = {}

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/get-key', methods=['GET'])
def get_key():
    new_key = generate_key()
    expiration_time = time.time() + 24 * 3600
    active_keys[new_key] = expiration_time
    return jsonify({'key': new_key})

@app.route('/api/verify-key/<key>', methods=['GET'])
def verify_key(key):
    current_time = time.time()
    if key in active_keys and active_keys[key] > current_time:
        return jsonify({'valid': True, 'message': 'Key hợp lệ!'})
    return jsonify({'valid': False, 'message': 'Key không hợp lệ hoặc đã hết hạn.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
