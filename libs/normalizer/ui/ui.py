import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QCheckBox, QMessageBox, QDialog, QScrollArea, QFrame, QLineEdit, QHBoxLayout,
    QWidget, QSpinBox, QInputDialog, QComboBox
)
from PyQt5.QtCore import Qt
from libs.normalizer.controllers.file_controller import FileController
from libs.normalizer.services.data_processor import DataProcessor
from controllers.preferences_controller import PreferencesController
from libs.normalizer.config.columns import columns

class ExcelProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Normalizador de Listas")
        self.setGeometry(100, 100, 600, 300)

        # Instances of separated logic
        self.data_processor = DataProcessor()
        self.file_manager = FileController(self.data_processor)

        # Variables
        self.process_by_sheets = True
        self.header_line = 1
        self.directoy_key = PreferencesController().dk_normalized

        # Opciones predefinidas para renombrar las columnas
        self.options = columns

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        self.label = QLabel("Escoge una o más opciones para comenzar", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.checkbox = QCheckBox("Procesar por hojas", self)
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.toggle_process_by_sheets)
        self.layout.addWidget(self.checkbox)

        self.upload_button = QPushButton("Subir archivos", self)
        self.upload_button.clicked.connect(self.upload_and_list_files)
        self.upload_button.setFixedHeight(30)
        self.layout.addWidget(self.upload_button)

    def toggle_process_by_sheets(self, state):
        self.process_by_sheets = state == Qt.Checked

    def upload_and_list_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Selecciona archivos Excel", "", "Excel files (*.xlsx *.xls)")
        if not file_paths:
            return

        self.file_manager.load_files(file_paths)

        if self.process_by_sheets:
            self.show_sheet_selection()
        else:
            self.process_next_file()

    def show_sheet_selection(self):
        for file in self.file_manager.file_names:
            sheet_names = self.file_manager.get_sheet_names(file)
            sheet_selection_dialog = QDialog(self)
            sheet_selection_dialog.setWindowTitle(f"Selecciona hojas para {file}")
            layout = QVBoxLayout(sheet_selection_dialog)

            checkboxes = []
            for sheet in sheet_names:
                checkbox = QCheckBox(sheet, sheet_selection_dialog)
                checkboxes.append(checkbox)
                layout.addWidget(checkbox)

            # SpinBox para seleccionar la línea de encabezado
            spin_box_label = QLabel("Línea de encabezado:", sheet_selection_dialog)
            layout.addWidget(spin_box_label)

            spin_box = QSpinBox(sheet_selection_dialog)
            spin_box.setMinimum(1)
            spin_box.setMaximum(100)
            spin_box.setValue(self.header_line)  # Valor inicial desde self.header_line
            layout.addWidget(spin_box)

            # Botón para procesar las hojas seleccionadas
            process_button = QPushButton("Procesar hojas seleccionadas", sheet_selection_dialog)
            process_button.clicked.connect(lambda: self.set_sheet_selection(
                file, checkboxes, sheet_names, sheet_selection_dialog, spin_box.value()
            ))
            layout.addWidget(process_button)

            sheet_selection_dialog.exec_()

    def set_sheet_selection(self, file, checkboxes, sheet_names, dialog, header_line):
        """
        Establece las hojas seleccionadas y la línea de encabezado para un archivo.
        """
        selected_sheets = [sheet for checkbox, sheet in zip(checkboxes, sheet_names) if checkbox.isChecked()]
        self.file_manager.set_sheet_selection(file, selected_sheets)
        self.header_line = header_line  # Actualiza self.header_line con el valor del SpinBox
        dialog.accept()
        self.process_next_file()


    def process_next_file(self):
        try:
            file_generator = self.file_manager.get_next_file()
            file, sheet = next(file_generator)
            self.read_header(file, sheet)
        except StopIteration:
            self.show_final_options()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar el siguiente archivo: {str(e)}")

    def read_header(self, file_name, sheet_name):
        header_row = self.header_line - 1
        df = self.file_manager.read_excel(file_name, sheet_name, header_row)

        if df.empty:
            QMessageBox.critical(self, "Error", f"El archivo {file_name} (Hoja: {sheet_name}) está vacío.")
            return

        self.data_processor.df = df
        self.create_columns_window(file_name, sheet_name)

    def create_columns_window(self, file_name, sheet_name):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Cabeceras del archivo {file_name} - Hoja: {sheet_name}")
        dialog.resize(900, 400)

        layout = QVBoxLayout(dialog)

        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        self.checkboxes = []

        # Crear checkboxes para cada columna
        for col in self.data_processor.df.columns:
            checkbox = QCheckBox(col, scroll_content)
            self.checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox)

        layout.addWidget(scroll_area)

        # Botón para agregar columnas seleccionadas
        add_button = QPushButton("Agregar columnas seleccionadas", dialog)
        add_button.clicked.connect(lambda: self.select_columns(dialog))
        layout.addWidget(add_button)

        dialog.exec_()

    def select_columns(self, dialog):
        try:
            self.selected_columns = []

            for index, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    # Obtén el nombre original de la columna
                    original_name = self.data_processor.df.columns[index]
                    # Almacena el nombre original de la columna seleccionada
                    self.selected_columns.append(original_name)

            if not self.selected_columns:
                QMessageBox.warning(self, "Advertencia", "No se seleccionaron columnas.")
                return

            # Actualiza la selección de columnas en el DataFrame
            self.data_processor.df_combined = self.data_processor.df[self.selected_columns]

            QMessageBox.information(self, "Éxito", "Columnas seleccionadas correctamente.")
            dialog.accept()
            self.show_final_options()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al seleccionar las columnas: {str(e)}")

    def show_final_options(self):
        final_dialog = QDialog(self)
        final_dialog.setWindowTitle("Opciones finales")
        layout = QVBoxLayout(final_dialog)

        generate_button = QPushButton("Generar archivo combinado", final_dialog)
        generate_button.clicked.connect(self.generate_combined_file)
        layout.addWidget(generate_button)

        reference_button = QPushButton("Agregar columna desde archivo de referencia", final_dialog)
        reference_button.clicked.connect(self.upload_reference_file)
        layout.addWidget(reference_button)

        final_dialog.close()

        final_dialog.exec_()
    
    def rename_columns_dialog(self, dataframe):
        """
        Abre un cuadro de diálogo que permite seleccionar nuevos nombres de columnas desde un dropdown.
        Trabaja directamente con el DataFrame pasado como argumento.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Estandarizar Nombre de Columnas")
        dialog.resize(400, 300)

        layout = QVBoxLayout()

        # Lista para almacenar los nuevos nombres
        new_column_names = []

        # Crear un dropdown para cada columna seleccionada
        for original_name in self.selected_columns:
            row_layout = QHBoxLayout()

            # Etiqueta con el nombre de la columna original
            label = QLabel(f"{original_name}:")
            row_layout.addWidget(label)

            # Dropdown con las opciones
            combo_box = QComboBox()
            combo_box.addItems(self.options)
            combo_box.setCurrentText(original_name)
            row_layout.addWidget(combo_box)

            # Agregar a la lista de nuevos nombres
            new_column_names.append((original_name, combo_box))

            layout.addLayout(row_layout)

        # Botón de confirmación
        btn_confirm = QPushButton("Confirmar")
        layout.addWidget(btn_confirm)

        dialog.setLayout(layout)

        renamed_columns = {}

        # Función para manejar el clic en "Confirmar"
        def confirm():
            nonlocal renamed_columns

            # Obtener los nuevos nombres seleccionados por el usuario
            renamed_columns = {original: combo.currentText() for original, combo in new_column_names}

            # Validar que no haya nombres duplicados
            if len(set(renamed_columns.values())) != len(renamed_columns):
                QMessageBox.warning(dialog, "Error", "No puede haber nombres de columnas duplicados.")
                renamed_columns = {}
                return

            # Aplicar los nuevos nombres al DataFrame pasado como argumento
            dataframe.rename(columns=renamed_columns, inplace=True)

            # Actualizar la lista de columnas seleccionadas con los nuevos nombres
            self.selected_columns = [renamed_columns[original] for original in self.selected_columns]

            # Cerrar el diálogo
            dialog.accept()

        # Conectar el botón a la función de confirmación
        btn_confirm.clicked.connect(confirm)

        # Ejecutar el diálogo
        dialog.exec_()

        return renamed_columns


    def generate_combined_file(self):
        if not self.data_processor.df_combined.empty:
            # Llama a la función de renombrado solo si hay columnas seleccionadas
            if not hasattr(self, 'selected_columns') or not self.selected_columns:
                QMessageBox.critical(self, "Error", "No se han seleccionado columnas para renombrar.")
                return

            renamed_columns = self.rename_columns_dialog(self.data_processor.df_combined)
            if renamed_columns:
                try:
                    # Renombrar las columnas usando los nuevos nombres
                    new_column_names = [renamed_columns[col] for col in self.data_processor.df_combined.columns]
                    self.data_processor.rename_columns(new_column_names)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al renombrar columnas: {e}")
                    return

            # Ordenar las columnas según self.options
            try:
                ordered_columns = [col for col in self.options if col in self.data_processor.df_combined.columns]
                remaining_columns = [col for col in self.data_processor.df_combined.columns if col not in self.options]
                self.data_processor.df_combined = self.data_processor.df_combined[ordered_columns + remaining_columns]
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al ordenar columnas: {e}")
                return

            self.file_manager.save_combined_file(self.directoy_key)

        else:
            QMessageBox.critical(self, "Error", "No hay datos para combinar.")

    def upload_reference_file(self):
        reference_file, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo de referencia", "", "Excel files (*.xlsx *.xls)")
        if reference_file:
            self.data_processor.load_reference_file(reference_file)
            self.create_reference_window()

    def create_reference_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Columnas de referencia")
        layout = QVBoxLayout(dialog)

        id_label = QLabel("Columna de EAN:", dialog)
        layout.addWidget(id_label)

        self.id_column_input = QLineEdit(dialog)
        layout.addWidget(self.id_column_input)

        column_label = QLabel("Columna a agregar:", dialog)
        layout.addWidget(column_label)

        self.column_to_add_input = QLineEdit(dialog)
        layout.addWidget(self.column_to_add_input)

        add_button = QPushButton("Agregar columna", dialog)
        add_button.clicked.connect(self.add_reference_column)
        layout.addWidget(add_button)

        dialog.exec_()

    def add_reference_column(self):
        try:
            id_column_index = int(self.id_column_input.text()) - 1
            column_to_add_index = int(self.column_to_add_input.text()) - 1

            updated_df, added_column = self.data_processor.add_reference_column(id_column_index, column_to_add_index)
            QMessageBox.information(self, "Éxito", f"La columna '{added_column}' se ha agregado correctamente.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingresa índices válidos para las columnas.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

