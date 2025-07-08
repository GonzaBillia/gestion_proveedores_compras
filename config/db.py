import pymysql
from config.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE, P_DB_DATABASE, P_DB_HOST, P_DB_PORT, P_DB_USER, P_DB_PASSWORD

def create_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL con PyMySQL.
    """
    try:
        # Convertir el puerto a int, si es que lo tenemos en string
        port = int(DB_PORT) if DB_PORT else 6613

        connection = pymysql.connect(
            host=DB_HOST,
            port=port,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_DATABASE,
            use_unicode=True,
            charset='utf8',
        )
        print("Conexión exitosa a MySQL")
        return connection

    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
def create_connection_plex():
    """
    Crea y devuelve una conexión a la base de datos MySQL con PyMySQL.
    """
    try:
        # Convertir el puerto a int, si es que lo tenemos en string
        port = int(P_DB_PORT) if P_DB_PORT else 3306

        connection = pymysql.connect(
            host=P_DB_HOST,
            port=port,
            user=P_DB_USER,
            password=P_DB_PASSWORD,
            db=P_DB_DATABASE,
            use_unicode=True,
            charset='utf8',
        )
        print("Conexión exitosa a MySQL")
        return connection

    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    """
    Cierra la conexión a la base de datos PyMySQL
    """
    try:
        if connection:
            connection.close()
            print("Conexión cerrada exitosamente.")
    except pymysql.MySQLError as e:
        print(f"Error al cerrar la conexión: {e}")