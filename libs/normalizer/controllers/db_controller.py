from libs.normalizer.queries.products_by_ean import P_BY_EAN
from config.db import create_connection, close_connection
import pandas as pd


def fetch_products_by_ean(ean_list):
    conn = create_connection()
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
                    p.IDProducto, 
                    p.Troquel, 
                    p.Codebar, 
                    p.Producto, 
                    p.idProveedor,
                    'S' AS EsCodigoPrincipal
                FROM 
                    productos AS p
                WHERE 
                    p.Codebar IN ({placeholders})

                UNION ALL

                SELECT 
                    p2.IDProducto, 
                    p2.Troquel, 
                    pc.Codebar, 
                    p2.Producto, 
                    p2.idProveedor,
                    'N' AS EsCodigoPrincipal
                FROM 
                    productoscodebars AS pc
                    INNER JOIN productos AS p2 ON p2.IDProducto = pc.IDProducto
                WHERE 
                    pc.Codebar IN ({placeholders})
                    AND pc.Codebar NOT IN (
                        SELECT Codebar FROM productos WHERE Codebar IN ({placeholders})
                    )
                """
            cursor.execute(query, tuple(ean_list) * 3)
            result = cursor.fetchall()
            print(result)  # <-- Debería traer datos si los EAN existen en tu base

        if not result:
            return pd.DataFrame(columns=["EAN", "IDProducto", "Troquel", "Producto", "idProveedor"])

        columns = ['IDProducto', 'Troquel', 'Codebar', 'Producto', 'idProveedor', 'EsCodigoPrincipal']
        db_df = pd.DataFrame(result, columns=columns)
        db_df = db_df.drop(columns=['EsCodigoPrincipal'])
        db_df = db_df.rename(columns={"Codebar": "EAN"})
        db_df = db_df.drop_duplicates(subset=["IDProducto"]) 
        db_df = db_df[db_df["idProveedor"].notnull() & (db_df["idProveedor"] != "")]
        return db_df

    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        raise

    finally:
        close_connection(conn)