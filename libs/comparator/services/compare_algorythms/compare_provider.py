import pandas as pd
from libs.comparator.controllers.db_controller import fetch_products_by_provider

def compare_by_provider(provider_df, id_provider):
    # Se encarga de mostrar todos los productos que estan a nombre de ese proveedor pero no aparecen en la lista, con el objetivo de ver como cambiar el precio, re categorizarlo, etc.

    products_df = fetch_products_by_provider(id_provider)

    print(products_df)

    # Asegurarnos de que las columnas 'IDProveedor' existan en ambos DataFrames
    if 'IDProveedor' not in provider_df.columns or 'IDProveedor' not in products_df.columns:
        print(provider_df.columns)
        print(products_df.columns)
        raise ValueError("Ambos DataFrames deben incluir una columna llamada 'IDProveedor'.")

    # Convertir las columnas 'IDProveedor' a string para evitar errores de tipo
    provider_df['IDProveedor'] = provider_df['IDProveedor'].astype(str)
    products_df['IDProveedor'] = products_df['IDProveedor'].astype(str)

    # Realizar un merge con indicador para identificar no coincidencias
    merge_result = pd.merge(products_df, provider_df, on=["IDProveedor","IDProducto"], how="outer", indicator=True)

    print(merge_result["_merge"].value_counts())

    solo_base_datos = merge_result[merge_result["_merge"] == "left_only"]

    return {
        'solo_base_datos': solo_base_datos
    }



