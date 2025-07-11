from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

def make_costs_report(df):
    """
    Renombra las columnas de un DataFrame y aplica estilos condicionales
    al exportar los datos a un archivo Excel.

    Args:
        df (pd.DataFrame): DataFrame original.
        output_path (str): Ruta donde se guardará el archivo Excel.
    """
    # Renombrar columnas
    dfc = df.rename(
        columns={
            'idproducto': 'ID Producto',
            'ean': 'EAN',
            'descripcion': 'Descripcion',
            'costo': 'Costo Quantio',
            'precio_costo': 'Costo Proveedor',
            'iva': 'IVA',
            'margen_pvp': 'Margen PVP'
        }
    )

    return dfc
