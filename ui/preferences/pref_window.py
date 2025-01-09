import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QSpacerItem, QSizePolicy
)
from ui.preferences.sections.directories_section import DirectoriesSection  # Importar la sección Directorios

class PreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferencias")
        self.resize(600, 400)

        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Frame para el contenido (lista de secciones + contenido de secciones)
        content_frame = QFrame()
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        # Lista de secciones a la izquierda
        self.section_list = QListWidget()
        self.section_list.addItem("Directorios")
        self.section_list.currentRowChanged.connect(self.display_section)

        # StackedWidget para la vista de secciones a la derecha
        self.stack = QStackedWidget()
        self.stack.addWidget(DirectoriesSection())  # Agregar la sección Directorios

        # Agregar widgets al layout de contenido
        content_layout.addWidget(self.section_list, 1)
        content_layout.addWidget(self.stack, 3)

        # Agregar el frame de contenido al layout principal
        main_layout.addWidget(content_frame)

        # Frame para los botones
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        # Establecer política de tamaño para evitar que el frame de botones se expanda verticalmente
        button_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Espaciador para empujar los botones hacia la derecha
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Botón "Cancelar"
        cancel_button = QPushButton("Cancelar")
        cancel_button.setFixedHeight(30)  # Reducir la altura del botón
        cancel_button.clicked.connect(self.close)

        # Botón "Guardar"
        save_button = QPushButton("Guardar")
        save_button.setFixedHeight(30)  # Reducir la altura del botón
        save_button.clicked.connect(self.save_preferences)

        # Agregar los botones al layout de botones
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        # Agregar el frame de botones al layout principal
        main_layout.addWidget(button_frame)

        # Seleccionar la primera sección por defecto
        self.section_list.setCurrentRow(0)

    def display_section(self, index):
        """
        Cambia la vista en función de la sección seleccionada en la lista
        y asegura que el elemento de la lista esté seleccionado.
        """
        if index >= 0:
            self.stack.setCurrentIndex(index)
            self.section_list.setCurrentRow(index)

    def save_preferences(self):
        """
        Lógica para guardar las preferencias.
        """
        print("Preferencias guardadas.")
        self.close()  # Cierra la ventana después de guardar