from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'retail_dashboard.db'

# Mock generate_sql function replaces real AI with hardcoded queries
def generate_sql(question):
    question = question.lower()
    if "total revenue" in question:
        return "SELECT SUM(revenue) AS total_revenue FROM sales;"
    if "all customers" in question:
        return "SELECT * FROM customers LIMIT 10;"
    if "all products" in question:
        return "SELECT * FROM products LIMIT 10;"
    if "sales trends" in question:
        return "SELECT salesdate, SUM(revenue) AS revenue FROM sales GROUP BY salesdate ORDER BY salesdate;"
    # Default fallback query
    return "SELECT * FROM customers LIMIT 5;"

def run_query(sql):
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        conn.close()

        results = [dict(zip(columns, row)) for row in rows]
        return results
    except Exception as e:
        return {"error": str(e)}

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_question = data.get('question')
    if not user_question:
        return jsonify({"error": "Question is required"}), 400

    sql_query = generate_sql(user_question)
    results = run_query(sql_query)

    return jsonify({
        "sql": sql_query,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
