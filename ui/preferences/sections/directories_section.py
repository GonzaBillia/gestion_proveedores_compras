from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from ui.preferences.components.accordion import Accordion
from ui.preferences.components.title_label import TitleLabel
from ui.preferences.components.divider import  Divider


class DirectoriesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Configura la interfaz de usuario de la sección Directorios.
        """
        # Layout principal
        layout = QVBoxLayout()

        # Título de la sección
        section_title = TitleLabel("Directorios de Destino")
        layout.addWidget(section_title)


        # Crear un divisor horizontal
        divider = Divider()

        # Crear el acordeón
        norm_fields = [
            ("Destino del Archivo Normalizado")
        ]
        accordion_normalizador = Accordion("Normalizador", norm_fields)

        comp_fields = [
            ("Destino de Archivos para Procesos"),
            ("Destino de Reportes")
        ]
        accordion_comparador = Accordion("Comparador", comp_fields)

        # Agregar el acordeón al layout principal
        layout.addWidget(accordion_normalizador)
        layout.addWidget(divider)
        layout.addWidget(accordion_comparador)

        # Ajustar el espaciado y los márgenes del layout
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Establecer el layout principal
        self.setLayout(layout)

    
