import pandas as pd

def format_maintance_report(df):
    columnas = ['idproducto', 'ean', 'precio_costo', 'pvp']

    dfm = df[columnas].copy()

    dfm.rename(
        columns={
            'idproducto': 'ID QUANTIO',
            'ean': 'EAN',
            'precio_costo': 'PRECIO_COSTO',
            'pvp': 'PVP'
        },
        inplace=True
    )

    return dfm


