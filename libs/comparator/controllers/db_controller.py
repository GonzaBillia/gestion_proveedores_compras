import pandas as pd
from config.db import create_connection, close_connection
from libs.comparator.queries.queries import PRODUCTS_MATCHED, ALL_CODEBARS, ALL_PROVIDERS, PRODUCTS_BY_PROVIDER
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_products_matched(array_productos):
    """
    Consulta a la base de datos para obtener los datos de productos.
    Devuelve un DataFrame con la información de la tabla.
    """
    connection = create_connection()
    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with connection.cursor() as cursor:
            logging.info("Ejecutando consulta: PRODUCTS_BY_PROVIDER")
            cursor.execute(PRODUCTS_MATCHED, {'id_producto_array': array_productos})
            result = cursor.fetchall()
        
        # Validar resultados
        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos

        columns = [
            "IDProducto",
            "ean",
            "descripcion",
            "Proveedor",
            "IDProveedor",
            "Laboratorio",
            "IDLaboratorio",
            "Costo",
            "iva",
            "precio_iva",
            "margen_pvp",
            "pvp",
            "Activo"
        ]
        db_df = pd.DataFrame(result, columns=columns)
        

        # Convertir resultados a DataFrame
        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise  # Propagar la excepción para que sea manejada por el nivel superior si es necesario

    finally:
        # Asegurarse de cerrar la conexión
        close_connection(connection)

def fetch_products_by_barcode():
    connection = create_connection()

    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with connection.cursor() as cursor:
            logging.info("Ejecutando consulta: ALL_CODEBARS")
            cursor.execute(ALL_CODEBARS)
            result = cursor.fetchall()
        
        # Validar resultados
        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos

        columns = ['IDProducto', 'ean', 'EsCodigoPrincipal']
        db_df = pd.DataFrame(result, columns=columns)

        # Convertir resultados a DataFrame
        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise  # Propagar la excepción para que sea manejada por el nivel superior si es necesario

    finally:
        # Asegurarse de cerrar la conexión
        close_connection(connection)

def fetch_all_providers():
    connection = create_connection()

    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with connection.cursor() as cursor:
            logging.info("Ejecutando consulta: PRODUCTS_BY_PROVIDER")
            cursor.execute(ALL_PROVIDERS)
            result = cursor.fetchall()
        
        # Validar resultados
        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos

        columns = ['IDProveedor', 'Nombre']
        db_df = pd.DataFrame(result, columns=columns)

        # Convertir resultados a DataFrame
        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise  # Propagar la excepción para que sea manejada por el nivel superior si es necesario

    finally:
        # Asegurarse de cerrar la conexión
        close_connection(connection)

def fetch_products_by_provider(id_provider):
    connection = create_connection()
    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with connection.cursor() as cursor:
            logging.info("Ejecutando consulta: PRODUCTS_BY_PROVIDER")
            cursor.execute(PRODUCTS_BY_PROVIDER, {'id_provider': id_provider})
            result = cursor.fetchall()
        
        # Validar resultados
        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos

        columns = ['IDProducto', 'ean', 'descripcion', 'Proveedor', 'IDProveedor', 'Laboratorio', 'IDLaboratorio', 'Activo']
        db_df = pd.DataFrame(result, columns=columns)

        # Convertir resultados a DataFrame
        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise  # Propagar la excepción para que sea manejada por el nivel superior si es necesario

    finally:
        # Asegurarse de cerrar la conexión
        close_connection(connection)