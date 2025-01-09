from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from ui.preferences.components.accordion import Accordion
from ui.preferences.components.title_label import TitleLabel
from ui.preferences.components.divider import Divider
from controllers.preferences_controller import PreferencesController


class DirectoriesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PreferencesController()
        self.accordion_normalizador = None
        self.accordion_comparador = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título de la sección
        section_title = TitleLabel("Directorios de Destino")
        layout.addWidget(section_title)

        # Crear un divisor horizontal
        divider = Divider()

        # Crear el acordeón para Normalizador
        self.accordion_normalizador = Accordion("Normalizador", [
            ("normalized_file_dir", "Destino del Archivo Normalizado")
        ])

        # Crear el acordeón para Comparador
        self.accordion_comparador = Accordion("Comparador", [
            ("comparator_processed_file_dir", "Destino de Archivos para Procesos"),
            ("reports_dir", "Destino de Reportes")
        ])

        # Agregar los widgets al layout principal
        layout.addWidget(self.accordion_normalizador)
        layout.addWidget(divider)
        layout.addWidget(self.accordion_comparador)

        # Ajustar el espaciado y los márgenes del layout
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Establecer el layout principal
        self.setLayout(layout)

        # Cargar los datos existentes
        self.load_data()

    def load_data(self):
        """
        Carga los valores desde el archivo JSON y los muestra en los inputs de ambos acordeones.
        """
        preferences = self.controller.load_preferences()
        directories = preferences.get("directories", {})

        for key, input_field in self.accordion_normalizador.inputs.items():
            input_field.setText(directories.get(key, ""))

        for key, input_field in self.accordion_comparador.inputs.items():
            input_field.setText(directories.get(key, ""))

    def collect_data(self):
        """
        Recolecta los datos de los inputs de ambos acordeones y los retorna como un diccionario.
        """
        data = {
            "directories": {}
        }

        # Recolectar datos del acordeón Normalizador
        for key, input_field in self.accordion_normalizador.inputs.items():
            data["directories"][key] = input_field.text()

        # Recolectar datos del acordeón Comparador
        for key, input_field in self.accordion_comparador.inputs.items():
            data["directories"][key] = input_field.text()

        return data
