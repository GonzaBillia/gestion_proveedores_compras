import pandas as pd

def format_codebar_report(df):
    """
    Selecciona las columnas especificadas de un DataFrame y retorna el DataFrame filtrado.
    
    Args:
        df (pd.DataFrame): El DataFrame original.

    Returns:
        pd.DataFrame: El DataFrame filtrado con las columnas especificadas.
    """
    df.rename(columns={
        'idproducto_1': 'idproducto',
        'ean_1': 'ean_proveedor',
        'ean_2': 'ean_quantio',
        'descripcion_2': 'descripcion'
    }, inplace=True)


    # Columnas que deseas seleccionar
    columnas = ['idproducto', 'ean_quantio', 'ean_proveedor', 'descripcion']

    # Filtrar el DataFrame con las columnas especificadas
    df_formateado = df[columnas].copy()

    # Filtrar filas donde `ean_quantio` y `ean_proveedor` no coincidan
    df_no_coinciden = df_formateado[df_formateado['ean_quantio'] != df_formateado['ean_proveedor']]

    # Retornar únicamente el DataFrame formateado
    return df_no_coinciden


