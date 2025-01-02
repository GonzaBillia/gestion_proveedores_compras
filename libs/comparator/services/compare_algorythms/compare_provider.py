import pandas as pd
from libs.comparator.controllers.db_controller import fetch_products_by_provider

def compare_by_provider(provider_df, id_provider):
    # Se encarga de mostrar todos los productos que estan a nombre de ese proveedor pero no aparecen en la lista, con el objetivo de ver como cambiar el precio, re categorizarlo, etc.

    products_df = fetch_products_by_provider(id_provider)
    products_df.columns = products_df.columns.str.lower()

    # Asegurarnos de que las columnas 'idproveedor' existan en ambos DataFrames
    if 'idproveedor' not in provider_df.columns or 'idproveedor' not in products_df.columns:
        print(provider_df.columns)
        print(products_df.columns)
        raise ValueError("Ambos DataFrames deben incluir una columna llamada 'idproveedor'.")

    # Convertir las columnas 'idproveedor' a string para evitar errores de tipo
    provider_df['idproveedor'] = provider_df['idproveedor'].astype(str)
    products_df['idproveedor'] = products_df['idproveedor'].astype(str)

    # Realizar un merge con indicador para identificar no coincidencias
    merge_result = pd.merge(products_df, provider_df, on=["idproveedor","idproducto"], how="outer", indicator=True)

    solo_base_datos = merge_result[merge_result["_merge"] == "left_only"]
    coincidencias = merge_result[merge_result["_merge"] == "both"]

    df_with_names = [
        (coincidencias, 'coincidencias'),
        (solo_base_datos, 'solo en base de datos')
    ]

    return df_with_names



