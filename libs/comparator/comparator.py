import pandas as pd
from libs.comparator.controllers.db_controller import fetch_products_by_provider
from libs.comparator.services.compare_algorythms.compare_ean import compare_by_barcode

def make_comparation():
    # Creating the DataFrame for the provider table from the data shared earlier
    provider_data = {
        "ean": [
            "7790550001024", "7790550010606", "7790550003417", "7790550003684", 
            "7790550000638", "7790550010705", "7790550010569", "7790550010415", 
            "7790550029127", "7790550022210", "7790550022234", "7790550022258",
            "7790550022272", "7790550022296", "7790550022319", "7790550022333", 
            "7790550022418", "7790550022432", "7790550022456", "7790550022470", 
            "7790550022494", "7790550000140", "7790550000157", "7790550000164", 
            "7790550000171", "7790550020230", "7790550011641", "7790550001307",
            "7790550011290", "7790550010255", "7790550012860", "7790550012808",
            "7790550012624", "7790550012686", "7790550029417", "7790550029431", 
            "7790550029455", "7790550029479", "7790550029493", "7790550029516", 
            "7790550029530", "7790550024054", "7790550000065", "7790550026454",
            "7790550026478", "7790550026492"
        ],
        "description": [
            "CAB GRANO SUPER 6x1000g", "CAB GRANO PRESTIGE 6x1000g", "CAB GRANO DO CERRADO 6x1000g", 
            "CAB GRANO AL GRANO 6x1000g", "CAB GRANO SABOR EQUILIBRADO 6x1000g", "CAB GRANO PEDRA AZUL 6x1000g", 
            "CAB GRANO COLOMBIA 6x1000g", "CAB GRANO PERU 6x1000g", "CAB GRANO AL GRANO 6X500g",
            "CAB MOLIDO SUPER 12x125g", "CAB MOLIDO SUPER 12x250g", "CAB MOLIDO SUPER 6x500g",
            "CAB MOLIDO PRESTIGE 12x250g", "CAB MOLIDO PRESTIGE 6x500g", "CAB MOLIDO HAPPY DAY 12x250g",
            "VITA MOLIDO 12x250g", "CAB MOLIDO COLOMBIA 12x250g", "CAB MOLIDO COLOMBIA 6x500g",
            "CAB MOLIDO PERU 12x250g", "CAB MOLIDO BRASIL 12x250g", "CAB MOLIDO BRASIL 6x500g",
            "LPC MOLIDO 12x125g", "LPC MOLIDO 12x250g", "LPC MOLIDO 6x500g",
            "LPC MOLIDO 6x1000g", "CAB MOLIDO AL GRANO 6x500g", "CAB MOLIDO HOSTELERIA 6x1000g",
            "CAB MOLIDO SABOR EQUILIBRADO 12x250g", "CAB SAQUITOS 18x18x5g", "LPC SAQUITOS 18x18x5g",
            "CAB SENSEO LPC 12x16x7g", "CAB SENSEO SUPER 12x16x7g", "CAB U ESPRESSO 6x20x7g",
            "CAB U ESPRESSO DESC 6x20x7g", "LPC SOLUBLE CLASICO 12x160g", "LPC SOLUBLE CLASICO 12x170g",
            "LPC SOLUBLE SUAVE 12x170g", "LPC SOLUBLE SUAVE 12x100g", "LPC SOLUBLE SUAVE 12x160g",
            "LPC SOLUBLE SUAVE 12x110g", "LPC SOLUBLE SUAVE 6x36x1.7g", "CAB SOLUBLE 25kg",
            "LPC CAPPUCCINO CLASICO 12x115g", "LPC CAPPUCCINO LATTE 12x115g", "LPC CAPPUCCINO MOKA 12x115g",
            "LPC CAPPUCCINO LIGHT 12x110g"
        ],
        "price": [
            35.487, 39.430, 35.487, 35.487, 20.199, 36.754, 40.855, 49.898, 17.997,
            2.623, 5.246, 10.492, 6.609, 13.218, 6.609, 8.260, 8.260, 16.520, 8.260, 
            8.260, 16.520, 1.462, 2.924, 5.849, 11.697, 5.849, 11.123, 4.025, 2.611, 
            2.331, 4.469, 4.749, 4.930, 6.130, 4.285, 4.908, 4.908, 2.887, 4.285, 
            2.946, 2.901, 651.496, 2.833, 2.833, 2.833, 2.833
        ]
    }
    provider_df = pd.DataFrame(provider_data)
    provider_df.columns = ['ean', 'Description', 'Price']

    db_df = fetch_products_by_provider()

    result = compare_by_barcode(provider_df, db_df)

    print("Coincidencias (matches):")
    print(result["matches"])

    print("\nProductos sin coincidencias (unmatched):")
    print(result["unmatched"])