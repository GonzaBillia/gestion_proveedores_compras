from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode, find_unmatches_barcodes, get_unique_providers
from libs.comparator.services.compare_algorythms.compare_provider import compare_by_provider
from libs.comparator.controllers.file_controller import read_file, normalize_columns, export_file_to_excel, pedir_ubicacion_archivo
from libs.comparator.services.reports.reports import make_report

def read_list(file_path):
from libs.comparator.services.compare_algorythms.compare_costs import make_cost_comparation
from libs.comparator.controllers.file_controller import read_file, normalize_columns, export_file_to_excel
from libs.comparator.ui.main_window import pedir_ubicacion_archivo

def make_comparation():
    # ARCHIVO Proveedor
    # temp
    provider_df_path, provider_name = pedir_ubicacion_archivo()
    # temp

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
    provider_df = read_list(provider_df)
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

    unmatched_cb = find_unmatches_barcodes(matches, matches_p)

    provider_datalist, provider_list = get_unique_providers(matches_p)

    matches_p_with_names = [
        (matches_p, 'Productos matched')
    ]
    unmatched_cb = find_unmatches_barcodes(matches, matches_p)
    update_ui_callback(3)
        (matches_p, 'Productos matched'),
        (provider_datalist, 'Proveedores Encontrados')
    ]

    cost_df = make_cost_comparation(matches_p, matches)

    cost_df_w_names = [
        (cost_df, 'Costos comparados')
    ]

    # Tarea 5: Guardar archivos procesados
    export_file_to_excel(result, 'resultados_avent.xlsx')
    export_file_to_excel(matches_p_with_names, 'matches_quantio_avent.xlsx')
    update_ui_callback(4)
    # Guardado de archivos
    export_file_to_excel(result, f'resultados_{provider_name}.xlsx')
    export_file_to_excel(matches_p_with_names, f'matches_quantio_{provider_name}.xlsx')
    export_file_to_excel(cost_df_w_names, f"comparacion_costos_{provider_name}.xlsx")

    return unmatched, matches_p, unmatched_cb, cost_df, provider_list, provider_name

def make_provider_comparation(provider_match, provider_list, provider_name):
    # Funcion de comparacion por proveedor

    result = compare_by_provider(provider_match, provider_list)

    export_file_to_excel(result, f'resultado_por_proveedor_{provider_name}.xlsx')

    return result[1][0]

def setup_report(matches_df, processed_matches_df, unmatched_cb, costs_df):
    report_array = [
        matches_df,
        processed_matches_df,
        unmatched_cb,
        costs_df
    ]

    return report_array

def process():
    # TEMP
    id_provider = 18

    unmatched, matches, unmatched_cb = make_comparation()

    quantio_matches_df = make_provider_comparation(matches, id_provider)

    df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb)

    make_report(df_array)

