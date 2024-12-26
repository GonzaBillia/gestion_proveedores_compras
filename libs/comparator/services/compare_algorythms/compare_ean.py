import pandas as pd

def compare_by_barcode(provider_df, db_df):
    """
    Compara los productos del proveedor con los productos de la base de datos utilizando el código de barras (EAN).
    Utiliza DataFrames de Pandas para trabajar con las tablas.

    :param provider_df: DataFrame de productos del proveedor (debe incluir la columna 'ean').
    :param db_df: DataFrame de productos de la base de datos (debe incluir la columna 'ean').
    :return: Diccionario con dos DataFrames: 'matches' (coincidencias) y 'unmatched' (sin coincidencias).
    """
    # Asegurarnos de que las columnas 'ean' existan en ambos DataFrames
    if 'ean' not in provider_df.columns or 'ean' not in db_df.columns:
        print(provider_df.columns)
        print(db_df.columns)
        raise ValueError("Ambos DataFrames deben incluir una columna llamada 'ean'.")

    # Convertir las columnas 'ean' a string para evitar errores de tipo
    provider_df['ean'] = provider_df['ean'].astype(str)
    db_df['ean'] = db_df['ean'].astype(str)

    

    # Encontrar coincidencias utilizando un merge por la columna 'ean'
    matches = pd.merge(provider_df, db_df, on='ean', how='inner', suffixes=('_provider', '_db'))

    # Encontrar productos sin coincidencias en el DataFrame del proveedor
    unmatched = provider_df.loc[~provider_df['ean'].isin(matches['ean'])]

    # Crear la lista de tuplas
    dataframes_with_names = [
        (matches, 'Matches'),  # Productos con coincidencias
        (unmatched, 'Unmatched')  # Productos sin coincidencias
    ]

    return dataframes_with_names
