import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manju@12345",
    database="cinematch"
)

cursor = db.cursor()

print("✅ CineMatch Database Connected")