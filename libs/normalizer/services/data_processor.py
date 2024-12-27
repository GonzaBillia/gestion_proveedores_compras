import pandas as pd


class DataProcessor:
    def __init__(self):
        """
        Inicializa el procesador de datos.
        """
        self.df_combined = pd.DataFrame()
        self.df = None  # DataFrame actual que se está procesando
        self.reference_df = None  # DataFrame de referencia

    def combine_dataframes(self, dfs):
        """
        Combina una lista de DataFrames en uno solo.
        :param dfs: Lista de DataFrames.
        :return: DataFrame combinado.
        """
        try:
            self.df_combined = pd.concat(dfs, ignore_index=True)
            return self.df_combined
        except Exception as e:
            print(f"Error al combinar los DataFrames: {e}")
            return pd.DataFrame()

    def filter_columns(self, df, columns):
        """
        Filtra columnas específicas de un DataFrame.
        :param df: DataFrame original.
        :param columns: Lista de columnas a incluir.
        :return: DataFrame filtrado.
        """
        try:
            return df[columns]
        except KeyError as e:
            print(f"Error al filtrar columnas: {e}")
            return pd.DataFrame()

    def read_file(self, file_name, sheet_name=None, header_row=0):
        """
        Lee un archivo Excel y retorna el DataFrame correspondiente.
        :param file_name: Ruta del archivo.
        :param sheet_name: Nombre de la hoja (opcional).
        :param header_row: Fila que se usará como encabezado.
        :return: DataFrame con los datos leídos.
        """
        try:
            if sheet_name:
                self.df = pd.read_excel(file_name, sheet_name=sheet_name, engine="openpyxl", header=header_row, dtype=str)
            else:
                self.df = pd.read_excel(file_name, engine="openpyxl", header=header_row, dtype=str)
            return self.df.reset_index(drop=True)
        except Exception as e:
            print(f"Error al leer el archivo {file_name}, Hoja: {sheet_name} -> {e}")
            return pd.DataFrame()

    def combine_columns(self, df, selected_columns_order):
        """
        Combina columnas seleccionadas y las agrega al DataFrame combinado.
        :param df: DataFrame original.
        :param selected_columns_order: Lista de tuplas (orden, índice de columna).
        :return: DataFrame combinado.
        """
        try:
            selected_columns = [df.iloc[:, idx[1]].copy() for idx in selected_columns_order]
            new_df = pd.concat(selected_columns, axis=1)
            new_df.columns = [f"Column_{i+1}" for i in range(len(new_df.columns))]

            if self.df_combined.empty:
                self.df_combined = new_df
            else:
                self.df_combined = pd.concat([self.df_combined, new_df], ignore_index=True)
            return self.df_combined
        except Exception as e:
            print(f"Error al combinar columnas: {e}")
            return pd.DataFrame()

    def load_reference_file(self, reference_file):
        """
        Carga un archivo de referencia en formato Excel.
        :param reference_file: Ruta del archivo de referencia.
        :return: DataFrame del archivo de referencia.
        """
        try:
            self.reference_df = pd.read_excel(reference_file, dtype=str)
            return self.reference_df
        except Exception as e:
            print(f"Error al cargar el archivo de referencia: {e}")
            return None

    def add_reference_column(self, id_column_index, column_to_add_index):
        """
        Agrega una columna del archivo de referencia al DataFrame combinado.
        :param id_column_index: Índice de la columna de ID.
        :param column_to_add_index: Índice de la columna a agregar.
        :return: DataFrame actualizado y nombre de la columna agregada.
        """
        try:
            if self.reference_df is None:
                raise ValueError("El archivo de referencia no está cargado.")

            # Validación de índices
            if id_column_index < 0 or id_column_index >= self.reference_df.shape[1]:
                raise IndexError(f"El índice de ID '{id_column_index}' está fuera de rango.")
            if column_to_add_index < 0 or column_to_add_index >= self.reference_df.shape[1]:
                raise IndexError(f"El índice de columna a agregar '{column_to_add_index}' está fuera de rango.")

            # Nombres de columnas
            id_column = self.reference_df.columns[id_column_index]
            column_to_add = self.reference_df.columns[column_to_add_index]

            # Merge
            self.df_combined = self.df_combined.merge(
                self.reference_df[[id_column, column_to_add]],
                left_on=self.df_combined.columns[0],  # Primera columna del combinado
                right_on=id_column,
                how="left"
            )

            # Limpieza
            self.df_combined.drop(columns=[id_column], inplace=True)
            self.df_combined.dropna(subset=[self.df_combined.columns[0]], inplace=True)

            return self.df_combined, column_to_add
        except Exception as e:
            print(f"Error al agregar la columna de referencia: {e}")
            raise

    def rename_columns(self, new_column_names):
        """
        Renombra las columnas del DataFrame combinado.
        :param new_column_names: Lista de nuevos nombres.
        """
        try:
            if self.df_combined.empty:
                raise ValueError("El DataFrame combinado está vacío.")
            self.df_combined.columns = new_column_names
        except Exception as e:
            print(f"Error al renombrar columnas: {e}")
            raise

    def save_combined_file(self, output_file):
        """
        Guarda el DataFrame combinado en un archivo Excel.
        :param output_file: Ruta del archivo de salida.
        """
        try:
            if self.df_combined.empty:
                raise ValueError("El DataFrame combinado está vacío.")
            self.df_combined.to_excel(output_file, index=False, header=True)
        except Exception as e:
            print(f"Error al guardar el archivo combinado: {e}")
            raise
