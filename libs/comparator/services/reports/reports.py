from datetime import datetime
from libs.comparator.services.reports.data_frames.missing_report import format_missing_report
from libs.comparator.services.reports.data_frames.barcode_report import format_codebar_report
from libs.comparator.services.reports.data_frames.provider_report import format_provider_report
from libs.comparator.controllers.file_controller import export_file_to_excel, format_costs_excel
from controllers.preferences_controller import PreferencesController

dk_reports = PreferencesController().dk_reports

def make_report(data_frame_array, update_ui_callback, req_filename_reporte, req_filename_costos, req_path_callback):
    missing_df = data_frame_array[0]
    provider_df = data_frame_array[1]
    codebar_df = data_frame_array[2]
    costs_df = data_frame_array[3]

    missing_report = format_missing_report(missing_df)
    codebar_report = format_codebar_report(codebar_df)
    provider_report = format_provider_report(provider_df)
    update_ui_callback(7)

    setup_report = [
        (missing_report, 'Posibles Incorporaciones'),
        (codebar_report, 'Codigos Principales Incorrectos'),
        (provider_report, 'Productos Solo en Base de Datos')
    ]

    setup_cost_report = [
        (costs_df, 'Comparacion de Costos')
    ]
    report = export_file_to_excel(setup_report, dk_reports, req_filename_reporte, req_path_callback)
    cost_report = export_file_to_excel(setup_cost_report, dk_reports, req_filename_costos, req_path_callback)
    format_costs_excel(cost_report)
    update_ui_callback(8)
