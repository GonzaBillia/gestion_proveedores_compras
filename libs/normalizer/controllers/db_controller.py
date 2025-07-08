from libs.normalizer.queries.products_by_ean import P_BY_EAN
from config.db import create_connection_plex, close_connection
import pandas as pd

def fetch_providers():
    conn = create_connection_plex()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()
    
    try:
        with cursor:
            query = f"""
                SELECT CodProve, Razon FROM proveedores;
            """
            
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        raise
    finally:
        close_connection(conn)

def fetch_products_by_ean(ean_list):
    conn = create_connection_plex()
    if conn is None:
        raise Exception("❌ No se pudo conectar a la base de datos. Verifique los parámetros de conexión.")
    cursor = conn.cursor()

    try:
        with cursor:
            if not ean_list:
                return pd.DataFrame(columns=["EAN", "IDProducto", "Troquel", "Producto", "idProveedor", 'EsCodigoPrincipal'])
            placeholders = ','.join(['%s'] * len(ean_list))
            query = f"""
                SELECT 
                    p.CodPlex, 
                    p.Troquel, 
                    p.Codebar, 
                    p.Producto, 
                    p.idProveedor,
                    'S' AS EsCodigoPrincipal
                FROM 
                    medicamentos AS p
                WHERE 
                    p.Codebar IN ({placeholders})
                """
            cursor.execute(query, tuple(ean_list))
            result = cursor.fetchall()

        if not result:
            return pd.DataFrame(columns=["EAN", "IDProducto", "Troquel", "Producto", "idProveedor"])

        columns = ['IDProducto', 'Troquel', 'Codebar', 'Producto', 'idProveedor', 'EsCodigoPrincipal']
        db_df = pd.DataFrame(result, columns=columns)
        db_df = db_df.drop(columns=['EsCodigoPrincipal'])
        db_df = db_df.rename(columns={"Codebar": "EAN"})
        db_df = db_df.rename(columns={"CodPlex": "IDProducto"})
        db_df = db_df.drop_duplicates(subset=["IDProducto"]) 
        db_df = db_df[db_df["idProveedor"].notnull() & (db_df["idProveedor"] != "")]
        
        return db_df

    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        raise

    finally:
        close_connection(conn)