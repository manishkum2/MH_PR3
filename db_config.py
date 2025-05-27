
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",        
            user="root",      
            password="root@39",      
            database="hospital"      
        )
        if connection.is_connected():
            print(" Database connection established successfully.")
            return connection
    except Error as e:
        print(f" Error while connecting to MySQL: {e}")
        return None

get_db_connection()
# cursor = conn.cursor()
# cursor.execute("SHOW TABLES;")
# for table in cursor.fetchall():
#     print(table[0])


