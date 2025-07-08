import pandas as pd
from config.db import create_connection, close_connection
from libs.comparator.queries.queries import PRODUCTS_MATCHED, ALL_CODEBARS, ALL_PROVIDERS
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_products_matched(array_productos):
    """
    Consulta a la base de datos para obtener los datos de productos.
    Devuelve un DataFrame con la información de la tabla.
    """
    conn = create_connection()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()
    try:
        logging.info("Estableciendo conexión a la base de datos.")

        # --- Control de nulos ---
        productos_limpios = [p for p in array_productos if p is not None]
        if len(productos_limpios) < len(array_productos):
            logging.warning("Se encontraron valores nulos en la lista de productos, fueron ignorados.")
        if not productos_limpios:
            logging.warning("No hay productos válidos para buscar.")
            return pd.DataFrame()

        # Armado de placeholders y query
        placeholders = ', '.join(['%s'] * len(productos_limpios))
        query = f"""
            SELECT 
                p.IDProducto,
                p.Codebar AS ean,
                CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
                pr.Nombre AS Proveedor,
                pr.IDProveedor AS IDProveedor,
                l.Nombre AS Laboratorio,
                p.IDLaboratorio,
                p.Costo,
                CASE 
                    WHEN p.idTipoIVA = 2 THEN 10.5
                    WHEN p.idTipoIVA = 3 THEN 21
                    WHEN p.idTipoIVA = 4 THEN 27
                    ELSE 0
                END AS iva,
                p.Costo + (p.Costo * CASE 
                    WHEN p.idTipoIVA = 2 THEN 0.105
                    WHEN p.idTipoIVA = 3 THEN 0.21
                    WHEN p.idTipoIVA = 4 THEN 0.27
                    ELSE 0
                END) AS precio_iva,
                p.MargenPVP AS margen_pvp,
                ROUND((p.Costo + (p.Costo * CASE 
                    WHEN p.idTipoIVA = 2 THEN 0.105
                    WHEN p.idTipoIVA = 3 THEN 0.21
                    WHEN p.idTipoIVA = 4 THEN 0.27
                    ELSE 0
                END)) * (1 + p.MargenPVP / 100), 2) AS pvp,
                p.Activo
            FROM 
                productos AS p
            INNER JOIN 
                laboratorios AS l ON p.IDLaboratorio = l.IDLaboratorio
            INNER JOIN 
                proveedores AS pr ON p.IDProveedor = pr.IDProveedor
            WHERE 
                p.IDProducto IN ({placeholders})
        """

        with cursor:
            cursor.execute(query, productos_limpios)
            result = cursor.fetchall()

        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()

        columns = [
            "IDProducto", "ean", "descripcion", "Proveedor", "IDProveedor",
            "Laboratorio", "IDLaboratorio", "Costo", "iva", "precio_iva",
            "margen_pvp", "pvp", "Activo"
        ]
        db_df = pd.DataFrame(result, columns=columns)
        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise

    finally:
        close_connection(conn)


def fetch_products_by_barcode():
    conn = create_connection()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()

    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with cursor:
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
        close_connection(conn)

def fetch_all_providers():
    conn = create_connection()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()

    try:
        logging.info("Estableciendo conexión a la base de datos.")
        # Ejecutar la consulta
        with cursor:
            logging.info("Ejecutando consulta: ALL_PROVIDERS")
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
        close_connection(conn)

def fetch_products_by_provider(id_provider):
    conn = create_connection()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()
    try:
        logging.info("Estableciendo conexión a la base de datos.")
        with cursor:
            logging.info("Ejecutando consulta: PRODUCTS_BY_PROVIDER")
            base_query = """
                SELECT 
                    p.IDProducto,
                    p.Codebar AS ean,
                    CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
                    pr.Nombre AS Proveedor,
                    pr.IDProveedor AS IDProveedor,
                    l.Nombre AS Laboratorio,
                    p.IDLaboratorio,
                    p.Activo
                FROM 
                    productos AS p
                INNER JOIN 
                    laboratorios AS l
                    ON p.IDLaboratorio = l.IDLaboratorio
                INNER JOIN 
                    proveedores AS pr
                    ON p.IDProveedor = pr.IDProveedor
            """
            params = {}
            if id_provider:
                base_query += "\nWHERE pr.IDProveedor = %(id_provider)s"
                params['id_provider'] = id_provider

            # El execute debe recibir los params solo si existen
            if params:
                cursor.execute(base_query, params)
            else:
                cursor.execute(base_query)

            result = cursor.fetchall()

        # Validar resultados
        if not result:
            logging.warning("La consulta no devolvió resultados.")
            return pd.DataFrame()

        columns = ['IDProducto', 'ean', 'descripcion', 'Proveedor', 'IDProveedor', 'Laboratorio', 'IDLaboratorio', 'Activo']
        db_df = pd.DataFrame(result, columns=columns)

        logging.info("Transformando resultados a DataFrame.")
        return db_df

    except Exception as e:
        logging.error(f"Error al obtener datos de la base de datos: {e}")
        raise

    finally:
        close_connection(conn)
