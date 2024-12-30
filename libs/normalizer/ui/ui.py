import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QCheckBox, QMessageBox, QDialog, QScrollArea, QFrame, QLineEdit, QHBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt
from libs.normalizer.controllers.file_controller import FileController
from libs.normalizer.services.data_processor import DataProcessor

class ExcelProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Processor")
        self.setGeometry(100, 100, 900, 500)

        # Instances of separated logic
        self.file_manager = FileController()
        self.data_processor = DataProcessor()

        # Variables
        self.process_by_sheets = False
        self.header_line = 1

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        self.label = QLabel("Escoge una o más opciones", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.checkbox = QCheckBox("Procesar por hojas", self)
        self.checkbox.stateChanged.connect(self.toggle_process_by_sheets)
        self.layout.addWidget(self.checkbox)

        self.upload_button = QPushButton("Subir archivos", self)
        self.upload_button.clicked.connect(self.upload_and_list_files)
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

            process_button = QPushButton("Procesar hojas seleccionadas", sheet_selection_dialog)
            process_button.clicked.connect(lambda: self.set_sheet_selection(file, checkboxes, sheet_names, sheet_selection_dialog))
            layout.addWidget(process_button)

            sheet_selection_dialog.exec_()

    def set_sheet_selection(self, file, checkboxes, sheet_names, dialog):
        selected_sheets = [sheet for checkbox, sheet in zip(checkboxes, sheet_names) if checkbox.isChecked()]
        self.file_manager.set_sheet_selection(file, selected_sheets)
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
        self.order_inputs = []

        for col in self.data_processor.df.columns:
            checkbox = QCheckBox(col, scroll_content)
            self.checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox)

            order_input = QLineEdit(scroll_content)
            order_input.setPlaceholderText("Orden")
            self.order_inputs.append(order_input)
            scroll_layout.addWidget(order_input)

        layout.addWidget(scroll_area)

        add_button = QPushButton("Agregar columnas seleccionadas", dialog)
        add_button.clicked.connect(lambda: self.select_columns(dialog))
        layout.addWidget(add_button)

        dialog.exec_()

    def select_columns(self, dialog):
        try:
            selected_columns_order = sorted(
                [
                    (int(order.text()), index)
                    for index, order in enumerate(self.order_inputs)
                    if self.checkboxes[index].isChecked() and order.text().isdigit()
                ]
            )

            if not selected_columns_order:
                QMessageBox.warning(self, "Advertencia", "No se seleccionaron columnas o no se asignaron órdenes válidas.")
                return

            combined_df = self.data_processor.combine_columns(self.data_processor.df, selected_columns_order)

            if combined_df.empty:
                QMessageBox.critical(self, "Error", "No se pudieron combinar las columnas seleccionadas.")
                return

            QMessageBox.information(self, "Éxito", "Columnas agregadas correctamente.")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar las columnas: {str(e)}")

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

        final_dialog.exec_()

    def generate_combined_file(self):
        if not self.data_processor.df_combined.empty:
            output_file, _ = QFileDialog.getSaveFileName(self, "Guardar archivo combinado", "", "Excel files (*.xlsx)")
            if output_file:
                self.data_processor.save_combined_file(output_file)
                QMessageBox.information(self, "Éxito", f"Archivo combinado guardado en: {output_file}")
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

