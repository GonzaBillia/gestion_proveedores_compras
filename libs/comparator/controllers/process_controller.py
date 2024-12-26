from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode
from libs.comparator.services.compare_algorythms.compare_provider import compare_by_provider
from libs.comparator.controllers.file_controller import read_file, open_file, normalize_columns, export_file_to_excel

def make_comparation():
    # ARCHIVO Proveedor
    # temp
    provider_df_path = open_file()
    # temp

    # Lectura y limpieza de archivo
    provider_df = read_file(provider_df_path)
    provider_df = normalize_columns(provider_df)
    provider_df = provider_df.drop_duplicates(subset='ean')

    # Lectura y limpieza de archivo
    db_df = fetch_products_by_barcode()
    db_df = normalize_columns(db_df)
    db_df = db_df.drop_duplicates(subset='ean')

    # Funcion de comparacion por Codigo de Barras
    result = compare_by_barcode(provider_df, db_df)

    matches = result[0][0]
    unmatched = result[1][0]

    # Impresion de resultados por consola
    print("Coincidencias (matches):")
    print(matches)

    print("\nProductos sin coincidencias (unmatched):")
    print(unmatched)

    # Obtencion de IDs para segunda consulta
    array_productos = matches["idproducto"].tolist()

    # Consulta de productos coincidentes con lista de proveedor
    matches_p = fetch_products_matched(array_productos)

    matches_p_with_names = [
        (matches_p, 'Productos matched')
    ]

    # Guardado de archivos
    export_file_to_excel(result, 'resultados_avent.xlsx')
    export_file_to_excel(matches_p_with_names, 'matches_quantio_avent.xlsx')

    return matches_p

def make_provider_comparation(provider_match, id_provider):
    # Funcion de comparacion por proveedor

    result = compare_by_provider(provider_match, id_provider)

    print("\nProductos que solo están en tu base de datos:")
    print(result[1][0])

    export_file_to_excel(result, 'resultado_por_proveedor_avent.xlsx')