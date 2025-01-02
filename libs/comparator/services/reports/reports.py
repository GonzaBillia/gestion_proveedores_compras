from datetime import datetime
from libs.comparator.services.reports.data_frames.missing_report import format_missing_report
from libs.comparator.services.reports.data_frames.barcode_report import format_codebar_report
from libs.comparator.services.reports.data_frames.provider_report import format_provider_report
from libs.comparator.controllers.file_controller import export_file_to_excel, format_costs_excel

def make_report(data_frame_array, provider_name):
    missing_df = data_frame_array[0]
    provider_df = data_frame_array[1]
    codebar_df = data_frame_array[2]
    costs_df = data_frame_array[3]

    missing_report = format_missing_report(missing_df)
    codebar_report = format_codebar_report(codebar_df)
    provider_report = format_provider_report(provider_df)

    setup_report = [
        (missing_report, 'Posibles Incorporaciones'),
        (codebar_report, 'Codigos Principales Incorrectos'),
        (provider_report, 'Productos Solo en Base de Datos')
    ]

    setup_cost_report = [
        (costs_df, 'Comparacion de Costos')
    ]
    report = export_file_to_excel(setup_report, f'reporte_{provider_name}_{datetime.today().strftime('%Y-%m-%d')}.xlsx')
    cost_report = export_file_to_excel(setup_cost_report, f"reporte_costos_{provider_name}_{datetime.today().strftime('%Y-%m-%d')}.xlsx")
    
    format_costs_excel(cost_report)
