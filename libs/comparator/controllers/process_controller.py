from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode, find_unmatches_barcodes, get_unique_providers
from libs.comparator.services.compare_algorythms.compare_provider import compare_by_provider
from libs.comparator.controllers.file_controller import read_file, normalize_columns, export_file_without_ask
from controllers.preferences_controller import PreferencesController
from libs.comparator.services.compare_algorythms.compare_costs import make_cost_comparation

pref_controller = PreferencesController()
dk_reports = pref_controller.dk_reports

def make_comparation(provider_path, update_ui_callback):
    """
    Función que realiza el proceso de comparación paso a paso.
    Actualiza la UI mediante el callback proporcionado.
    
    :param provider_df: DataFrame de productos del proveedor.
    :param update_ui_callback: Función para actualizar la UI.
    :return: unmatched, matches_p, unmatched_cb.
    """
    provider_df, file_name = read_file(provider_path)
    provider_df = normalize_columns(provider_df)
    provider_df = provider_df.drop_duplicates(subset='ean')
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

    update_ui_callback(3)

    matches_p_with_names = [
        (matches_p, 'Coincidencias'),
        (provider_datalist, 'Proveedores Encontrados')
    ]

    cost_df = make_cost_comparation(matches_p, matches)

    cost_df_w_names = [
        (cost_df, 'Costos comparados')
    ]

    # Guardado de archivos
    export_file_without_ask(result, file_name, "coincidencias")
    export_file_without_ask(matches_p_with_names, file_name, "coincidencias_base")
    export_file_without_ask(cost_df_w_names, file_name, "costos_base")
    update_ui_callback(4)

    return unmatched, matches_p, unmatched_cb, cost_df, provider_list, file_name

def make_provider_comparation(provider_match, provider_list, update_ui_callback, file_name):
    # Funcion de comparacion por proveedor

    result = compare_by_provider(provider_match, provider_list)
    update_ui_callback(5)

    export_file_without_ask(result, file_name, "proveedores")
    update_ui_callback(6)

    return result[1][0]

def setup_report(matches_df, processed_matches_df, unmatched_cb, costs_df):
    report_array = [
        matches_df,
        processed_matches_df,
        unmatched_cb,
        costs_df
    ]

    return report_array


