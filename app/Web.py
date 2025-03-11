from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Kết nối Database
def get_db():
    conn = sqlite3.connect("users.db")
    return conn, conn.cursor()

# API kiểm tra & cộng coin
@app.route("/api/check-payment", methods=["POST"])
def check_payment():
    data = request.json
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")

    conn, cursor = get_db()

    # Tìm giao dịch trong đơn nạp
    cursor.execute("SELECT user_id FROM deposits WHERE transaction_id = ? AND amount = ?", (transaction_id, amount))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        cursor.execute("UPDATE users SET coin = coin + ? WHERE user_id = ?", (amount, user_id))
        cursor.execute("DELETE FROM deposits WHERE transaction_id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Cộng coin thành công!"})
    
    conn.close()
    return jsonify({"success": False, "message": "Giao dịch không hợp lệ hoặc đã xử lý."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# Định nghĩa app
app = Flask(__name__)
