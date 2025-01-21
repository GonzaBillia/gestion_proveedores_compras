import pandas as pd

def compare_by_barcode(provider_df, db_df):
    """
    Compara los productos del proveedor con los productos de la base de datos utilizando el código de barras (EAN).
    Utiliza DataFrames de Pandas para trabajar con las tablas.

    :param provider_df: DataFrame de productos del proveedor (debe incluir la columna 'ean').
    :param db_df: DataFrame de productos de la base de datos (debe incluir la columna 'ean').
    :return: Lista de tuplas con dos DataFrames: 'Matches' (coincidencias) y 'Unmatched' (sin coincidencias).
    """

    # 1. Convertir a string y unificar para evitar conflictos (quita el .0 del final)
    provider_df['ean'] = (
        provider_df['ean']
        .astype(str)
        .str.replace(r'\.0$', '', regex=True)
        .str.strip()
    )
    db_df['ean'] = (
        db_df['ean']
        .astype(str)
        .str.replace(r'\.0$', '', regex=True)
        .str.strip()
    )

    # 2. Si existe la columna 'id_quantio', intentamos rellenar ean vacío a partir de 'id_quantio'
    if 'id_quantio' in provider_df.columns:
        provider_df.rename(columns={'id_quantio': 'idproducto'}, inplace=True)

        # Asegurarnos de que la columna idproducto exista también en db_df
        # (puede que necesites renombrar la columna en db_df, o verificar que exista)
        if 'idproducto' not in db_df.columns and 'id_quantio' in db_df.columns:
            db_df.rename(columns={'id_quantio': 'idproducto'}, inplace=True)

        # Máscara de filas sin ean (vacío, '-', 'nan', etc.)
        mask_no_ean = (
            (provider_df['ean'].isna()) |
            (provider_df['ean'] == '')  |
            (provider_df['ean'] == '-') |
            (provider_df['ean'] == 'nan')
        )

        # Filtramos sólo las filas que no tienen ean
        provider_no_ean = provider_df.loc[mask_no_ean].copy()

        # Si db_df también tiene idproducto, completamos
        if 'idproducto' in db_df.columns:
            provider_no_ean = provider_no_ean.merge(
                db_df[['idproducto', 'ean']], 
                on='idproducto', 
                how='left', 
                suffixes=('', '_db')
            )

            # Actualizamos el ean vacío con el ean_db
            provider_df.loc[mask_no_ean, 'ean'] = provider_no_ean['ean_db']

    # 3. Limpiamos de nuevo por si se agregaron ean con “.0” del merge (raro, pero por seguridad)
    provider_df['ean'] = (
        provider_df['ean']
        .astype(str)
        .str.replace(r'\.0$', '', regex=True)
        .str.strip()
    )

    # 4. Ahora que provider_df tiene ean (ya sea original o rellenado),
    #    encontramos coincidencias con db_df (merge por 'ean')
    matches = pd.merge(provider_df, db_df, on='ean', how='inner', suffixes=('_provider', '_db'))
    matches.rename(columns={'idproducto_db': 'idproducto'}, inplace=True)

    # 5. Identificamos los productos sin coincidencias
    unmatched = provider_df.loc[~provider_df['ean'].isin(matches['ean'])]

    # 6. Retornamos la lista de tuplas (DataFrame, Nombre)
    dataframes_with_names = [
        (matches,   'Matches'), 
        (unmatched, 'Unmatched')
    ]

    return dataframes_with_names


def compare_by_id(provider_df, db_df):
    """
    Compara los productos del proveedor con los productos de la base de datos utilizando el código de barras (EAN).
    Utiliza DataFrames de Pandas para trabajar con las tablas.

    :param provider_df: DataFrame de productos del proveedor (debe incluir la columna 'ean').
    :param db_df: DataFrame de productos de la base de datos (debe incluir la columna 'ean').
    :return: Diccionario con dos DataFrames: 'matches' (coincidencias) y 'unmatched' (sin coincidencias).
    """
    # 1. Convertir a string para evitar errores de tipo
    provider_df.rename(columns={'id_quantio': 'idproducto'}, inplace=True)

    # 2. Ahora que provider_df tiene ean donde se pudo rellenar, 
    #    encontramos coincidencias (matches) con db_df
    matches = pd.merge(provider_df, db_df, on='idproducto', how='inner', suffixes=('_provider', '_db'))

    # 3. Identificamos los productos sin coincidencias
    unmatched = provider_df.loc[~provider_df['idproducto'].isin(matches['idproducto'])]

    # Crear la lista de tuplas
    dataframes_with_names = [
        (matches, 'Matches'),  # Productos con coincidencias
        (unmatched, 'Unmatched')  # Productos sin coincidencias
    ]

    return dataframes_with_names

def find_unmatches_barcodes(provider_df, db_df):

    db_df.columns = db_df.columns.str.lower()
    
    # Hacer el merge preservando todas las columnas de ambos DataFrames
    df_merge = pd.merge(provider_df, db_df, on='idproducto', how='outer', suffixes=('_1', '_2'))

    return df_merge

def get_unique_providers(df):
    """
    Obtiene los valores únicos de la columna 'idproveedor' y los valores correspondientes
    de la columna 'proveedor', y los guarda en un array.

    Args:
        df (pd.DataFrame): El DataFrame que contiene las columnas 'idproveedor' y 'proveedor'.

    Returns:
        list: Una lista de tuplas con valores únicos (idproveedor, proveedor).
    """
    # Eliminar duplicados basándose en 'idproveedor' y conservar el primero encontrado
    unique_providers = df[['idproveedor', 'proveedor']].drop_duplicates(subset=['idproveedor'])


    # Convertir a una lista de tuplas (idproveedor, proveedor)
    provider_list = unique_providers.values.tolist()
    print(provider_list)

    return unique_providers, provider_list