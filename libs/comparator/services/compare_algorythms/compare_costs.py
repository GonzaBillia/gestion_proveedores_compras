import pandas as pd

def make_cost_comparation(db_df, provider_df):
    """
    Compara costos entre dos DataFrames basado en la columna IDProducto.
    
    Args:
        db_df (pd.DataFrame): DataFrame principal que contiene información de productos.
        provider_df (pd.DataFrame): DataFrame del proveedor con costos de productos.

    Returns:
        pd.DataFrame: Un DataFrame con la comparación de costos.
    """
    try:
        # Realizar el merge en la columna IDProducto
        merged_df = pd.merge(db_df[["idproducto", "descripcion", "costo"]], provider_df[["idproducto", "precio_costo"]], on="idproducto", how="inner")
        
        # Seleccionar las columnas requeridas
        result_df = merged_df[["idproducto", "descripcion", "costo", "precio_costo"]]

        
        # Retornar el DataFrame resultante para uso posterior
        return result_df
    
    except KeyError as e:
        print(f"Error: columna no encontrada - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")