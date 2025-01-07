import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTableView, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExcelViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vista Previa de Excel")
        self.resize(1000, 600)

        # Layout principal
        self.layout = QVBoxLayout()

        # Crear QTableView
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

        # Botones
        self.load_button = QPushButton("Cargar Archivo Excel")
        self.save_button = QPushButton("Guardar Cambios")

        # Conectar botones a funciones
        self.load_button.clicked.connect(self.load_excel)
        self.save_button.clicked.connect(self.save_excel)

        # Layout para botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)

        # Agregar QTableView y botones al layout principal
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.table_view)

        # Establecer el layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_excel(self):
        """Función para cargar un archivo Excel y mostrarlo en el QTableView."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar Excel", "", "Archivos Excel (*.xlsx *.xls)")
        if file_path:
            df = pd.read_excel(file_path)
            self.show_dataframe(df)

    def show_dataframe(self, df):
        """Mostrar un DataFrame de pandas en el QTableView."""
        self.model.clear()
        self.model.setRowCount(df.shape[0])
        self.model.setColumnCount(df.shape[1])
        self.model.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, col]))
                self.model.setItem(row, col, item)

    def save_excel(self):
        """Función para guardar los cambios realizados en la tabla."""
        rows = self.model.rowCount()
        cols = self.model.columnCount()

        # Crear una lista de listas con los datos de la tabla
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.model.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data, columns=[self.model.horizontalHeaderItem(col).text() for col in range(cols)])

        # Guardar el archivo Excel
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Excel", "", "Archivos Excel (*.xlsx)")
        if file_path:
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Éxito", "Archivo guardado correctamente.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelViewer()
    window.show()
    sys.exit(app.exec_())
