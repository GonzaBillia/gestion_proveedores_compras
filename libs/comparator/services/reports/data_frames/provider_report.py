import pandas as pd

def format_provider_report(df):
    """
    Selecciona las columnas especificadas de un DataFrame y retorna el DataFrame filtrado.
    
    Args:
        df (pd.DataFrame): El DataFrame original.

    Returns:
        pd.DataFrame: El DataFrame filtrado con las columnas especificadas.
    """

    # Filtrar por productos activos
    df_activos = df[df['activo_x'] == 'S']

    # Columnas que deseas seleccionar
    columnas = ['idproducto', 'ean_x', 'descripcion_x', 'proveedor_x', 'laboratorio_x']

    # Filtrar el DataFrame con las columnas especificadas
    df_formateado = df_activos[columnas].copy()

    # Ordenar por 'laboratorio_x'
    df = df_formateado.sort_values(by='laboratorio_x')

    # Crear una lista para almacenar las filas con los saltos
    result_rows = []
    previous_value = None

    # Iterar sobre las filas del DataFrame
    for _, row in df.iterrows():
        # Si el valor cambia, agregar una fila vacía
        if previous_value is not None and row['laboratorio_x'] != previous_value:
            result_rows.append({col: None for col in df.columns})
        
        # Agregar la fila actual
        result_rows.append(row.to_dict())
        previous_value = row['laboratorio_x']

    # Crear el DataFrame final con los saltos
    df_result = pd.DataFrame(result_rows)

    # Renombrar las columnas
    df_result.rename(
        columns={
            'idproducto': 'ID Producto',
            'ean_x': 'EAN',
            'descripcion_x': 'Descripcion',
            'proveedor_x': 'Proveedor',
            'laboratorio_x': 'Laboratorio'
        },
        inplace=True
    )

    # Retornar únicamente el DataFrame formateado
    return df_result
