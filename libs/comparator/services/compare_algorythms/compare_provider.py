import pandas as pd
from libs.comparator.controllers.db_controller import fetch_products_by_provider

def compare_by_provider(provider_df, provider_list):
    """
    Compara los productos asociados a cada proveedor en la lista contra los productos en el DataFrame.
    
    Args:
        provider_df (pd.DataFrame): DataFrame que contiene los productos y sus proveedores.
        provider_list (list): Lista de tuplas con (idproveedor, proveedor).

    Returns:
        list: Una lista de tuplas con los DataFrames resultantes y el nombre del proveedor asociado.
    """
    if not provider_list:  # Si la lista está vacía, detener la ejecución
        raise ValueError("La lista de proveedores está vacía.")
    
    all_results = []

    for idproveedor, proveedor in provider_list:
        print(f"Procesando proveedor: {proveedor} (ID: {idproveedor})")
        
        products_df = fetch_products_by_provider(idproveedor)
        products_df.columns = products_df.columns.str.lower()

        if products_df.empty:  # Verificar si el DataFrame está vacío
            print(f"No se encontraron productos para el proveedor: {proveedor}")
            continue

        if 'idproveedor' not in provider_df.columns or 'idproveedor' not in products_df.columns:
            print(provider_df.columns)
            print(products_df.columns)
            raise ValueError("Ambos DataFrames deben incluir una columna llamada 'idproveedor'.")

        provider_df['idproveedor'] = provider_df['idproveedor'].astype(str)
        products_df['idproveedor'] = products_df['idproveedor'].astype(str)

        merge_result = pd.merge(products_df, provider_df, on=["idproveedor", "idproducto"], how="outer", indicator=True)
        print(merge_result.columns)
        # Filtrar solo las filas donde 'activo' sea igual a 'S'
        merge_result = merge_result[merge_result['activo_x'] == 'S']

        solo_base_datos = merge_result[merge_result["_merge"] == "left_only"]
        coincidencias = merge_result[merge_result["_merge"] == "both"]

        all_results.append((coincidencias, f"coincidencias_{proveedor}"))
        all_results.append((solo_base_datos, f"solo_base_datos_{proveedor}"))

    return all_results





