from libs.comparator.controllers.process_controller import make_comparation, make_provider_comparation

id_provider = 18

def comparate():
    matches = make_comparation()

    make_provider_comparation(matches, id_provider)