import pandas as pd
from libs.normalizer.config.columns import ITG_REQUIRED_COLUMNS
from libs.normalizer.controllers.db_controller import fetch_products_by_ean
import logging, os

# Configurar el logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def prepare(df):
    
    prods = fetch_products_by_ean(df["EAN"].tolist())
    print(prods)
    df = pd.merge(df, prods, how="left", on="EAN")
    
    return df


def execute(df, combined_path, filename, prov_id):
    # Asegura que EAN es str
    df["EAN"] = df["EAN"].astype(str)

    # Unir info de productos
    df["idProveedor"] = prov_id
    
    # Crear DataFrame final con columnas requeridas
    itg_df = pd.DataFrame({
        "id proveedor": df.get("idProveedor", ""),  # O ajusta si no viene de prods
        "codigo interno de proveedor": df.get("Troquel", ""),          # Si tienes este dato, ponlo aquí
        "cod bar": df["EAN"],
        "descripcion": df["DESCRIPCION"],
        "costo sin iva": df["PRECIO_COSTO"],
    }, columns=ITG_REQUIRED_COLUMNS)

    # Determinar carpeta de salida
    output_dir = os.path.dirname(combined_path) if combined_path else os.getcwd()
    itg_path = os.path.join(output_dir, f"{filename}_ITG.xlsx")

    # Exportar a Excel
    itg_df.to_excel(itg_path, index=False)

    return itg_path
