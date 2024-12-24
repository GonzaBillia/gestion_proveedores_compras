from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode
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

    # Impresion de resultados por consola
    print("Coincidencias (matches):")
    print(result["matches"])

    print("\nProductos sin coincidencias (unmatched):")
    print(result["unmatched"])

    # Obtencion de IDs para segunda consulta
    array_productos = result["matches"]["idproducto"].tolist()

    # Consulta de productos coincidentes con lista de proveedor
    matches = fetch_products_matched(array_productos)

    # Guardado de archivos
    export_file_to_excel(result["matches"], result["unmatched"], 'resultados-cabrales.xlsx')
    export_file_to_excel(matches, None, 'matches_quantio-cabrales.xlsx')