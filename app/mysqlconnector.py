import os
from mysql.connector import Error, connect

# Define function that connects to mySQL database server and returns the connection objectdef create_connection(host_name, user_name, user_password):
def create_connection():
    print("Attempt to create connection")
    connection = None
    db_host = os.getenv('DB_HOST')
    print(f"host: {db_host}")
    db_user = os.getenv('DB_USER')
    print(f"user: {db_user}")
    db_password = os.getenv('DB_PASSWORD')
    print(f"pw provided")
    db_name = os.getenv('DB_NAME')
    print(f"db name: {db_name}")

    try:
        connection = connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            database=db_name
        )
        print("Connection created!")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# cursor = connection.cursor()

# connection.close()