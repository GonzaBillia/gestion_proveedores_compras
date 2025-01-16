import pandas as pd
import numpy as np

def merge_and_format(cost_df, matches_df):
    # Merge de los dos DataFrames en base a la columna 'idproducto'
    merged_df = pd.merge(cost_df[['idproducto', 'precio_costo']], matches_df[['idproducto', 'ean', 'descripcion', 'iva', 'margen_pvp']], on='idproducto')
    
    merged_df['precio_costo'] = merged_df['precio_costo'].astype(float)
    merged_df['iva'] = merged_df['iva'].astype(float)
    merged_df['margen_pvp'] = merged_df['margen_pvp'].astype(float)

    return merged_df[['idproducto', 'ean', 'descripcion', 'precio_costo', 'iva', 'margen_pvp']]

def aplicar_formula(precio_iva, margen_pvp):
    """
    Aplica la fórmula para calcular el PVP formateado y redondeado hacia arriba.

    Args:
        precio_iva (float): Precio con IVA del producto.
        margen_pvp (int or float): Margen del PVP en porcentaje (ejemplo: 25 para un 25%).

    Returns:
        str: Resultado redondeado, formateado con coma como separador decimal.
    """
    if pd.isna(precio_iva) or pd.isna(margen_pvp) or precio_iva == '' or margen_pvp == '':
        return ''
    try:
        precio_iva = float(precio_iva)
        margen = 1 + (float(margen_pvp) / 100)  # Convertir el margen a factor

        # Aplicar el cálculo del PVP
        resultado = np.ceil(precio_iva * margen / 10) * 10  # Redondeo hacia arriba

        # Formatear el resultado con 3 decimales
        return f"{resultado:.3f}".replace('.', ',')
    except Exception as e:
        print(f"Error en aplicar fórmula: {e}")
        return ''

def calculate_pvp(merged_df):
    """
    Calcula el precio con IVA y el PVP considerando el margen, aplicando la fórmula con formateo.

    Args:
        merged_df (pd.DataFrame): DataFrame combinado con las columnas necesarias.

    Returns:
        pd.DataFrame: DataFrame con columnas calculadas 'precio_iva' y 'pvp'.
    """
    # Calcular el precio con IVA
    merged_df['precio_iva'] = merged_df['precio_costo'] * (1 + merged_df['iva'] / 100)

    # Calcular el PVP considerando el margen sobre el precio con IVA, usando aplicar_formula
    merged_df['pvp'] = merged_df.apply(lambda row: aplicar_formula(row['precio_iva'], row['margen_pvp']), axis=1)

    return merged_df[['idproducto', 'ean', 'descripcion', 'precio_costo', 'iva', 'margen_pvp', 'precio_iva', 'pvp']]
