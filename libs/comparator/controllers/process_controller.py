from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode, find_unmatches_barcodes
from libs.comparator.services.compare_algorythms.compare_provider import compare_by_provider
from libs.comparator.controllers.file_controller import read_file, normalize_columns, export_file_to_excel, pedir_ubicacion_archivo
from libs.comparator.services.reports.reports import make_report

def read_list(file_path):
    # Lectura y limpieza de archivo
    provider_df = read_file(file_path)
    provider_df = normalize_columns(provider_df)
    provider_df = provider_df.drop_duplicates(subset='ean')

    return provider_df

def make_comparation(provider_df, update_ui_callback):
    """
    Función que realiza el proceso de comparación paso a paso.
    Actualiza la UI mediante el callback proporcionado.
    
    :param provider_df: DataFrame de productos del proveedor.
    :param update_ui_callback: Función para actualizar la UI.
    :return: unmatched, matches_p, unmatched_cb.
    """
    # Tarea 1: Traer productos desde la base de datos
    db_df = fetch_products_by_barcode()
    update_ui_callback(0)  # Actualizar la UI después de la tarea

    # Tarea 2: Normalizar y limpiar datos
    db_df = normalize_columns(db_df)
    db_df = db_df.drop_duplicates(subset='ean')
    update_ui_callback(1)

    # Tarea 3: Comparar con la lista recibida
    result = compare_by_barcode(provider_df, db_df)
    matches = result[0][0]
    unmatched = result[1][0]

    # Obtener IDs para la segunda consulta
    array_productos = matches["idproducto"].tolist()
    update_ui_callback(2)

    # Tarea 4: Ordenar lista de productos
    matches_p = fetch_products_matched(array_productos)
    matches_p_with_names = [
        (matches_p, 'Productos matched')
    ]
    unmatched_cb = find_unmatches_barcodes(matches, matches_p)
    update_ui_callback(3)

    # Tarea 5: Guardar archivos procesados
    export_file_to_excel(result, 'resultados_avent.xlsx')
    export_file_to_excel(matches_p_with_names, 'matches_quantio_avent.xlsx')
    update_ui_callback(4)

    return unmatched, matches_p, unmatched_cb

def make_provider_comparation(provider_match, id_provider):
    # Funcion de comparacion por proveedor

    result = compare_by_provider(provider_match, id_provider)

    print("\nProductos que solo están en tu base de datos:")
    print(result[1][0])

    export_file_to_excel(result, 'resultado_por_proveedor_avent.xlsx')

    return result[1][0]

def setup_report(matches_df, processed_matches_df, unmatched_cb):
    report_array = [
        matches_df,
        processed_matches_df,
        unmatched_cb
    ]

    return report_array

def process():
    # TEMP
    id_provider = 18

    unmatched, matches, unmatched_cb = make_comparation()

    quantio_matches_df = make_provider_comparation(matches, id_provider)

    df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb)

    make_report(df_array)