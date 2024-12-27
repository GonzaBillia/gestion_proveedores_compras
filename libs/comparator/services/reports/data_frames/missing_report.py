import pandas as pd

def format_missing_report(df):
    """
    Selecciona las columnas especificadas de un DataFrame y retorna un nuevo DataFrame.
    
    Args:
        df (pd.DataFrame): El DataFrame original.
        columnas (list): Lista de nombres de las columnas a seleccionar.

    Returns:
        pd.DataFrame: Un nuevo DataFrame con las columnas seleccionadas.
    """
    columnas = ['ean', 'descripcion', 'precio_costo']

    # Filtrar el DataFrame con las columnas especificadas
    df_formateado = df[columnas].copy()

    # Crear una fila de encabezado combinando los nombres de las columnas
    encabezado = [" | ".join(columnas)] + [""] * (len(columnas) - 1)

    # Crear un DataFrame para el encabezado
    df_encabezado = pd.DataFrame([encabezado], columns=columnas)

    # Concatenar el encabezado con el DataFrame original
    df_resultado = pd.concat([df_encabezado, df_formateado], ignore_index=True)

    df_return = [
        (df_resultado, 'Posibles Incorporaciones')
    ]

    return df_return