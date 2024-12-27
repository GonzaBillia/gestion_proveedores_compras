import pandas as pd

def format_missing_report(df):
    """
    Selecciona las columnas especificadas de un DataFrame y retorna el DataFrame filtrado.
    
    Args:
        df (pd.DataFrame): El DataFrame original.

    Returns:
        pd.DataFrame: El DataFrame filtrado con las columnas especificadas.
    """
    # Columnas que deseas seleccionar
    columnas = ['ean', 'descripcion', 'precio_costo']

    # Filtrar el DataFrame con las columnas especificadas
    df_formateado = df[columnas].copy()

    # Retornar únicamente el DataFrame formateado
    return df_formateado


