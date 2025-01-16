import pandas as pd

import pandas as pd

def make_cost_comparation(db_df, provider_df):
    """
    Compara costos entre dos DataFrames basado en la columna 'idproducto'.
    
    Args:
        db_df (pd.DataFrame): DataFrame principal que contiene información de productos.
        provider_df (pd.DataFrame): DataFrame del proveedor con costos de productos.

    Returns:
        pd.DataFrame: Un DataFrame con la comparación de costos (con o sin 'pvp_sugerido', según disponibilidad).
    """
    try:
        # Definimos las columnas a incluir en el merge
        provider_columns = ["idproducto", "precio_costo"]
        
        # Si existe 'pvp_sugerido', la añadimos al merge
        if "pvp_sugerido" in provider_df.columns:
            provider_columns.append("pvp_sugerido")
        
        # Realizar el merge en la columna 'idproducto'
        merged_df = pd.merge(
            db_df[["idproducto", "ean", "descripcion", "costo"]],
            provider_df[provider_columns],
            on="idproducto",
            how="inner"
        )
        
        # Definimos las columnas que formarán parte del DataFrame resultante
        result_columns = ["idproducto", "ean", "descripcion", "costo", "precio_costo"]
        
        # Si existe 'pvp_sugerido', la añadimos al resultado
        if "pvp_sugerido" in provider_columns:
            result_columns.append("pvp_sugerido")
        
        result_df = merged_df[result_columns]

        # Convertir 'precio_costo' a float con 2 decimales
        result_df['precio_costo'] = result_df['precio_costo'].astype(float).round(2)
        
        # Si existe 'pvp_sugerido', también la convertimos a float con 2 decimales
        if "pvp_sugerido" in result_df.columns:
            result_df['pvp_sugerido'] = result_df['pvp_sugerido'].astype(float).round(2)

        # Retornar el DataFrame resultante para uso posterior
        return result_df
    
    except KeyError as e:
        print(f"Error: columna no encontrada - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
