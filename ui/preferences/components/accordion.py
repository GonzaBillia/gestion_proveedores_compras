from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QPushButton, QLabel, QLineEdit, QHBoxLayout, QFileDialog, QCheckBox


class Accordion(QWidget):
    def __init__(self, title, fields):
        """
        Crea un widget tipo acordeón que despliega los labels, inputs y checkboxes de manera dinámica.

        :param title: El título del acordeón.
        :param fields: Una lista de tuplas con el formato (field_key, label_text).
        """
        super().__init__()
        self.inputs = {}  # Diccionario para almacenar los inputs y checkboxes
        self.init_ui(title, fields)

    def init_ui(self, title, fields):
        # Botón de título del acordeón
        toggle_button = QPushButton(title)
        toggle_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                text-align: left;
                background-color: #f0f0f0;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        toggle_button.setCheckable(True)

        # Frame que contiene los widgets internos del acordeón
        content_frame = QFrame()
        content_frame.setVisible(False)

        # Layout interno del acordeón
        content_layout = QVBoxLayout()

        # Crear los inputs y checkboxes dinámicamente a partir de la lista de campos
        for field_key, label_text in fields:
            # Crear el label
            label = QLabel(label_text)

            # Crear el campo de entrada
            directory_input = QLineEdit()
            directory_input.setPlaceholderText(f"Selecciona el {label_text}")

            # Botón para abrir el selector de directorios
            browse_button = QPushButton("Buscar")
            browse_button.clicked.connect(lambda _, input_field=directory_input: self.select_directory(input_field))

            # Checkbox "Preguntar siempre"
            checkbox = QCheckBox("Preguntar siempre")

            # Guardar el input y el checkbox en el diccionario
            self.inputs[field_key] = {
                "input": directory_input,
                "checkbox": checkbox
            }

            # Layout horizontal para el input y el botón
            input_layout = QHBoxLayout()
            input_layout.addWidget(directory_input)
            input_layout.addWidget(browse_button)

            # Agregar los widgets al layout interno
            content_layout.addWidget(label)
            content_layout.addLayout(input_layout)
            content_layout.addWidget(checkbox)

        content_frame.setLayout(content_layout)
        toggle_button.toggled.connect(content_frame.setVisible)

        # Layout del acordeón (título + contenido)
        accordion_layout = QVBoxLayout()
        accordion_layout.addWidget(toggle_button)
        accordion_layout.addWidget(content_frame)

        self.setLayout(accordion_layout)

    def select_directory(self, input_field):
        """
        Abre un QFileDialog para seleccionar un directorio y muestra la ruta en el campo de entrada.
        """
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar directorio")
        if directory:
            input_field.setText(directory)

    def collect_data(self):
        """
        Recolecta los valores de los inputs y checkboxes y los retorna como un diccionario.
        """
        data = {}
        for field_key, widgets in self.inputs.items():
            data[field_key] = {
                "path": widgets["input"].text(),
                "ask": widgets["checkbox"].isChecked()
            }
        return data

    def load_data(self, preferences):
        """
        Carga los valores de los inputs y checkboxes desde un diccionario de preferencias.
        """
        for field_key, widgets in self.inputs.items():
            if field_key in preferences:
                widgets["input"].setText(preferences[field_key].get("path", ""))
                widgets["checkbox"].setChecked(preferences[field_key].get("ask", False))
