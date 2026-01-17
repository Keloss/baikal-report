import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="192.168.0.111",
        user="baikal",
        password="StrongPassword123!",
        database="baikal",
        auth_plugin="mysql_native_password"
    )
