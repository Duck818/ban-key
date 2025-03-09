# ban-key
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Trang web bán key đang hoạt động!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# C?u hình link API l?y key
KEY_API_URL = "https://flask-key-generator-1.onrender.com/api/generate-key"

# D? li?u gi? l?p tài kho?n ngu?i dùng
users = {
    "user1": {"balance": 10000, "purchased_keys": []},
    "user2": {"balance": 5000, "purchased_keys": []},
}

# Giá key theo th?i h?n
key_prices = {
    "1day": 5000,
    "3days": 15000,
    "7days": 30000,
    "30days": 120000  # Ðã gi?m giá t? 150000 xu?ng 120000
}

@app.route("/buy-key", methods=["POST"])
def buy_key():
    data = request.json
    username = data.get("username")
    key_type = data.get("key_type")
    
    if username not in users:
        return jsonify({"error": "Ngu?i dùng không t?n t?i!"}), 400
    
    if key_type not in key_prices:
        return jsonify({"error": "Lo?i key không h?p l?!"}), 400
    
    price = key_prices[key_type]
    if users[username]["balance"] < price:
        return jsonify({"error": "S? du không d?!"}), 400
    
    # Truy c?p API d? l?y key m?i
    response = requests.get(KEY_API_URL)
    if response.status_code == 200:
        new_key = response.json().get("key")
        users[username]["balance"] -= price
        users[username]["purchased_keys"].append({"key": new_key, "duration": key_type})
        return jsonify({"message": "Mua key thành công!", "key": new_key, "duration": key_type})
    else:
        return jsonify({"error": "Không th? l?y key t? h? th?ng!"}), 500

@app.route("/get-balance", methods=["GET"])
def get_balance():
    username = request.args.get("username")
    if username not in users:
        return jsonify({"error": "Ngu?i dùng không t?n t?i!"}), 400
    return jsonify({"balance": users[username]["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
