from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QCheckBox, QMessageBox, QDialog, QScrollArea, QFrame, QLineEdit, QHBoxLayout,
    QWidget, QSpinBox
)
from PyQt5.QtCore import Qt
from libs.comparator.ui.components.button import Button
from libs.comparator.controllers.process_controller import read_list

class ListComparator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mantenimiento de Base de Datos")
        self.setGeometry(100, 100, 600, 300)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()
    
    def create_widgets(self):
        self.label = QLabel("Compara una lista Normalizada y Genera reportes de Actualización", self)
        self.label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        self.button = QPushButton("Seleccionar Archivo", self)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        self.button.setMaximumWidth(150)
        self.button.clicked.connect(lambda: self.load_on_click())
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

    def load_on_click(self):
        file_path = self.pedir_ubicacion_archivo()
        if file_path is not None:
            print(f"Archivo seleccionado: {file_path}")  # Simulación del proceso
            p_df = read_list(file_path)

            self.button.deleteLater()  # Eliminar el botón de la UI
            success_label = QLabel("Archivo subido y leído", self)
            success_label.setAlignment(Qt.AlignHCenter)
            self.layout.addWidget(success_label, alignment=Qt.AlignCenter)

            Button.new(
            layout=self.layout,
            title="Procesar",
            width=150,
            align="center",
            command=lambda: print("Nuevo botón presionado")
            )

            return p_df
        else:
            return

    def pedir_ubicacion_archivo(parent=None):
        """
        Muestra un diálogo para que el usuario seleccione un archivo y retorna su ruta.
        
        :param parent: Ventana principal (opcional, puede ser None).
        :return: La ruta completa del archivo seleccionado o None si el usuario cancela.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Abrir en modo solo lectura (opcional)
        
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Seleccionar archivo",  # Título del diálogo
            "",                     # Directorio inicial (vacío para usar el predeterminado)
            "Archivos soportados (*.xlsx *.csv *.pdf *.txt);;Archivos de Excel (*.xlsx);;Archivos CSV (*.csv);;Archivos PDF (*.pdf);;Archivos de texto (*.txt)",  # Filtros
            options=options
        )
        
        return file_path if file_path else None
