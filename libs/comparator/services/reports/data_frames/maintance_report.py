

def format_maintance_report(df):
    if 'pvp_sugerido' in df.columns:
        df['pvp'] = df['pvp_sugerido']

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


