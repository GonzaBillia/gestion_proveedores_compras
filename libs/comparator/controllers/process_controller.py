from libs.comparator.controllers.db_controller import fetch_products_by_barcode, fetch_products_matched
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode, find_unmatches_barcodes, get_unique_providers
from libs.comparator.services.compare_algorythms.compare_provider import compare_by_provider
from libs.comparator.services.compare_algorythms.compare_costs import make_cost_comparation
from libs.comparator.controllers.file_controller import read_file, normalize_columns, export_file_to_excel
from libs.comparator.ui.main_window import pedir_ubicacion_archivo

def make_comparation():
    # ARCHIVO Proveedor
    # temp
    provider_df_path, provider_name = pedir_ubicacion_archivo()
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

    # Obtencion de IDs para segunda consulta
    array_productos = matches["idproducto"].tolist()

    # Consulta de productos coincidentes con lista de proveedor
    matches_p = fetch_products_matched(array_productos)

    unmatched_cb = find_unmatches_barcodes(matches, matches_p)

    provider_datalist, provider_list = get_unique_providers(matches_p)

    matches_p_with_names = [
        (matches_p, 'Productos matched'),
        (provider_datalist, 'Proveedores Encontrados')
    ]

    cost_df = make_cost_comparation(matches_p, matches)

    cost_df_w_names = [
        (cost_df, 'Costos comparados')
    ]

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

