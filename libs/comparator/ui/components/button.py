from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QCheckBox, QMessageBox, QDialog, QScrollArea, QFrame, QLineEdit, QHBoxLayout,
    QWidget, QSpinBox
)
from PyQt5.QtCore import Qt

class Button:
    @staticmethod
    def new(layout, title, width, align, command):
        """
        Crea un botón estilizado y lo agrega al layout con la alineación especificada.

        :param layout: Layout donde se agregará el botón.
        :param title: Texto del botón.
        :param width: Ancho máximo del botón.
        :param align: Alineación del botón ('center', 'Vcenter', 'Hcenter').
        :param command: Función a ejecutar al hacer clic en el botón.
        """
        if layout is None:
            raise ValueError("El layout no puede ser None. Asegúrate de pasar un layout válido.")


        button = QPushButton(title)
        button.setStyleSheet("""
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
        button.setMaximumWidth(width)
        button.clicked.connect(command)  # Ejecuta la función al hacer clic

        # Agregar el botón al layout con la alineación especificada
        if align == 'center':
            layout.addWidget(button, alignment=Qt.AlignCenter)
        elif align == 'Vcenter':
            layout.addWidget(button, alignment=Qt.AlignVCenter)
        else:
            layout.addWidget(button, alignment=Qt.AlignHCenter)

        return button  # Devuelve el botón creado por si se necesita acceso posterior

