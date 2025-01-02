from libs.comparator.controllers.process_controller import make_comparation, make_provider_comparation, setup_report
from libs.comparator.services.compare_algorythms.compare_costs import make_cost_comparation
from libs.comparator.services.reports.reports import make_report


def comparate():
    unmatched, matches, unmatched_cb, costs_df, provider_list, provider_name = make_comparation()

    quantio_matches_df = make_provider_comparation(matches, provider_list, provider_name)

    df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb, costs_df)

    make_report(df_array, provider_name)

    
