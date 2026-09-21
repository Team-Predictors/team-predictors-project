import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


db = get_db_connection()

print("Database connected successfully!")

cursor = db.cursor()
cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

print("Tables:", tables)

cursor.close()
db.close()