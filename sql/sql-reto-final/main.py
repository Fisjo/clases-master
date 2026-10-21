import os
import psycopg

url = os.getenv("DATABASE_URL")

try:
    with psycopg.connect(url) as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM videojuegos;")
            filas = cur.fetchall()

            for fila in filas:
                print(fila)
except Exception as e:
    print("Error:", e)
    raise
