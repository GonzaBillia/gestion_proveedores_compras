import pandas as pd
import numpy as np

def merge_and_format(cost_df, matches_df):
    """
    Realiza un merge de dos DataFrames en base a la columna 'idproducto',
    formatea los datos y opcionalmente incluye la columna 'pvp_sugerido' si está presente en cost_df.

    Args:
        cost_df (pd.DataFrame): DataFrame que contiene información de costos.
        matches_df (pd.DataFrame): DataFrame que contiene información adicional de productos.

    Returns:
        pd.DataFrame: DataFrame combinado y formateado.
    """
    # Determinar las columnas a incluir del cost_df
    cost_columns = ['idproducto', 'precio_costo']
    if 'pvp_sugerido' in cost_df.columns:
        cost_columns.append('pvp_sugerido')

    # Realizar el merge de los DataFrames
    merged_df = pd.merge(
        cost_df[cost_columns],
        matches_df[['idproducto', 'ean', 'descripcion', 'iva', 'margen_pvp']],
        on='idproducto'
    )
    
    # Formatear las columnas relevantes
    merged_df['precio_costo'] = merged_df['precio_costo'].astype(float)
    merged_df['iva'] = merged_df['iva'].astype(float)
    merged_df['margen_pvp'] = merged_df['margen_pvp'].astype(float)

    # Añadir 'pvp_sugerido' al resultado si estaba presente en el cost_df
    if 'pvp_sugerido' in cost_columns:
        return merged_df[['idproducto', 'ean', 'descripcion', 'precio_costo', 'iva', 'margen_pvp', 'pvp_sugerido']]
    else:
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

def calcular_margen_fila(precio_costo, pvp_sugerido, iva_porcentaje):
    """
    Calcula el margen del PVP para una fila específica.

    Args:
        precio_costo (float): Costo del producto.
        pvp_sugerido (float): Precio de venta sugerido.
        iva_porcentaje (float): Porcentaje de IVA (ejemplo: 21 para un 21% de IVA).

    Returns:
        float: Margen del PVP en porcentaje.
    """
    try:
        # Calcular el precio de costo con IVA
        costo_con_iva = precio_costo * (1 + iva_porcentaje / 100)
        
        # Calcular el margen en porcentaje
        margen = ((pvp_sugerido - costo_con_iva) / costo_con_iva) * 100  # Margen en porcentaje
        
        return round(margen, 2)  # Redondear a 2 decimales
    except Exception as e:
        print(f"Error al calcular margen: {e}")
        return None


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


def calcular_margen_pvp(df):
    """
    Calcula el margen del PVP considerando el precio costo, PVP sugerido, y el IVA.
    Luego calcula el precio con IVA y el PVP, agregando las columnas necesarias al DataFrame.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'precio_costo', 'pvp_sugerido', y 'iva'.

    Returns:
        pd.DataFrame: DataFrame con las columnas calculadas 'margen_pvp', 'precio_iva', y 'pvp'.
    """

    # Calcular el margen PVP
    df['margen_pvp'] = df.apply(
        lambda row: calcular_margen_fila(row['precio_costo'], row['pvp_sugerido'], row['iva']),
        axis=1
    )
    
    # Calcular el precio con IVA
    df['precio_iva'] = df['precio_costo'] * (1 + df['iva'] / 100)

    # Calcular el PVP considerando el margen sobre el precio con IVA, usando aplicar_formula
    df['pvp_sugerido'] = df.apply(lambda row: aplicar_formula(row['precio_iva'], row['margen_pvp']), axis=1)

    # Retornar las columnas solicitadas
    return df[['idproducto', 'ean', 'descripcion', 'precio_costo', 'iva', 'margen_pvp', 'precio_iva', 'pvp_sugerido']]

