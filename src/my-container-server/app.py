from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route("/items")
def get_items():
    conn = psycopg2.connect(
        dbname="mydb",
        user="giacomo",
        password="giacomo_password",
        host="db"  # nome del servizio DB nel docker-compose
    )
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items;")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": i[0], "name": i[1]} for i in items])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
