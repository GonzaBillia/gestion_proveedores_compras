import logging
import pandas as pd
import os

def setup_logger():
    """Setup logger for the file controller."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("file_controller.log"),
            logging.StreamHandler()
        ]
    )

setup_logger()

def open_file():
    """Open a file by prompting the user for its path."""
    try:
        file_path = input("Enter the file path to open: ")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        logging.info(f"File opened successfully: {file_path}")
        return file_path
    except FileNotFoundError as e:
        logging.error(f"Error opening file: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error opening file: {e}")
        return None

def save_file():
    """Prompt the user for a destination path to save a file."""
    try:
        destination_path = input("Enter the destination path to save the file: ")
        directory = os.path.dirname(destination_path)
        if directory and not os.path.exists(directory):
            raise FileNotFoundError(f"The directory {directory} does not exist.")
        logging.info(f"File destination selected: {destination_path}")
        return destination_path
    except FileNotFoundError as e:
        logging.error(f"Error selecting file destination: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error selecting file destination: {e}")
        return None

def read_file(file_path):
    """Read a file and return its content as a DataFrame if applicable."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".csv":
            df = pd.read_csv(file_path)
            logging.info(f"CSV file read successfully: {file_path}")
            return df
        elif file_extension == ".xlsx":
            df = pd.read_excel(file_path)
            logging.info(f"Excel file read successfully: {file_path}")
            return df
        else:
            with open(file_path, 'r') as file:
                content = file.read()
            logging.info(f"Text file read successfully: {file_path}")
            return content
    except FileNotFoundError as e:
        logging.error(f"Error reading file: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        logging.error(f"The file is empty or corrupted: {file_path} - {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading file: {e}")
        return None
    
def normalize_columns(df):
    """
    Normaliza las columnas de un DataFrame:
    - Elimina espacios iniciales y finales.
    - Convierte los nombres de las columnas a minúsculas.

    :param df: DataFrame a normalizar.
    :return: DataFrame con columnas normalizadas.
    """
    df.columns = df.columns.str.strip().str.lower()
    return df

def export_file(dataframe, filename, file_format='excel', sheet_name='Sheet1'):
    """
    Exporta un DataFrame a un archivo en el formato especificado.

    Args:
        dataframe (pd.DataFrame): El DataFrame a exportar.
        filename (str): Nombre del archivo a exportar (sin extensión).
        file_format (str): Formato del archivo ('excel', 'csv'). Default: 'excel'.
        sheet_name (str): Nombre de la hoja (solo aplica para Excel). Default: 'Sheet1'.
    """
    if file_format.lower() == 'excel':
        # Exportar como archivo Excel
        full_filename = f"{filename}.xlsx"
        dataframe.to_excel(full_filename, index=False, sheet_name=sheet_name)
    elif file_format.lower() == 'csv':
        # Exportar como archivo CSV
        full_filename = f"{filename}.csv"
        dataframe.to_csv(full_filename, index=False)
    else:
        raise ValueError("Formato no soportado. Usa 'excel' o 'csv'.")

    print(f"Archivo exportado: {full_filename}")

def export_file_to_excel(matches, unmatched, filename):
    path = 'C:\\Users\\Administrador\\Documents\\Gonzalo\\archivos\\lista proveedores\\comparados\\'
    """
    Exporta los DataFrames de `matches` y `unmatched` a un archivo Excel con hojas separadas.

    Args:
        matches (pd.DataFrame): DataFrame con los matches.
        unmatched (pd.DataFrame): DataFrame con los unmatched.
        filename (str): Nombre del archivo Excel a exportar. Default: 'results.xlsx'.
    """

    # Exportar a Excel
    with pd.ExcelWriter((path + filename), engine='openpyxl') as writer:
        # Verificar y exportar los matches si existen
        if matches is not None and not matches.empty:
            matches.to_excel(writer, index=False, sheet_name='Matches')
        else:
            print("El DataFrame 'matches' está vacío o no existe.")
        
        # Verificar y exportar los unmatched si existen
        if unmatched is not None and not unmatched.empty:
            unmatched.to_excel(writer, index=False, sheet_name='Unmatched')
        else:
            print("El DataFrame 'unmatched' está vacío o no existe.")
        print(f"Archivo exportado: {filename}")