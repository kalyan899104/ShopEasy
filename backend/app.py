from flask import Flask
import psycopg2

app = Flask(__name__)

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="shopeasy",
    user="postgres",
    password="postgres"
)


@app.route("/")
def home():
    return "Welcome to ShopEasy API version 2"


@app.route("/health")
def health():
    return {
        "status": "UP"
    }


@app.route("/db-health")
def db_health():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()

        return {
            "database": "UP"
        }

    except Exception as e:
        return {
            "database": "DOWN",
            "error": str(e)
        }, 500


@app.route("/products")
def products():

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products"
    )

    rows = cursor.fetchall()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2]
        })

    cursor.close()

    return products


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)