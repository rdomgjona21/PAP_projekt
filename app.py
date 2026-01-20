from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "data/laptop_data.db"


def query_db(query):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.route("/api/laptops", methods=["GET"])
def get_all_laptops():
    data = query_db("SELECT * FROM laptop_battery_analysis")
    return jsonify(data)


@app.route("/api/laptops/<company>", methods=["GET"])
def get_laptops_by_company(company):
    query = f"""
    SELECT * FROM laptop_battery_analysis
    WHERE LOWER(Company) = LOWER('{company}')
    """
    data = query_db(query)
    return jsonify(data)
@app.route("/")
def home():
    return {
        "message": "PAP Laptop Battery REST API",
        "endpoints": [
            "/api/laptops",
            "/api/laptops/<company>"
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)