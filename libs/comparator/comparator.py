from libs.comparator.controllers.process_controller import make_comparation, make_provider_comparation, setup_report
from libs.comparator.services.reports.reports import make_report


def comparate():
    unmatched, matches, unmatched_cb, provider_list = make_comparation()

    quantio_matches_df = make_provider_comparation(matches, provider_list)

    df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb)

    make_report(df_array)