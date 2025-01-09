from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QPushButton, QLabel, QLineEdit, QHBoxLayout, QFileDialog


class Accordion(QWidget):
    def __init__(self, title, fields):
        """
        Crea un widget tipo acordeón que despliega los labels e inputs de manera dinámica.

        :param title: El título del acordeón.
        :param fields: Una lista de strings con los nombres de los campos (label_text).
        """
        super().__init__()
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
                border-bottom: 1px solid gray;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        toggle_button.setCheckable(True)

        # Frame que contiene los widgets internos del acordeón
        content_frame = QFrame()
        content_frame.setVisible(False)  # Inicialmente oculto

        # Layout interno del acordeón
        content_layout = QVBoxLayout()

        # Crear los inputs dinámicamente a partir de la lista de campos
        for label_text in fields:
            # Crear el label
            label = QLabel(label_text)

            # Crear el campo de entrada
            directory_input = QLineEdit()

            # Botón para abrir el selector de directorios
            browse_button = QPushButton("Buscar")
            browse_button.clicked.connect(lambda _, input_field=directory_input: self.select_directory(input_field))

            # Layout horizontal para el input y el botón
            input_layout = QHBoxLayout()
            input_layout.addWidget(directory_input)
            input_layout.addWidget(browse_button)

            # Agregar los widgets al layout interno
            content_layout.addWidget(label)
            content_layout.addLayout(input_layout)

        # Establecer el layout en el frame
        content_frame.setLayout(content_layout)

        # Conectar el botón para mostrar/ocultar el contenido
        toggle_button.toggled.connect(content_frame.setVisible)

        # Layout del acordeón (título + contenido)
        accordion_layout = QVBoxLayout()
        accordion_layout.addWidget(toggle_button)
        accordion_layout.addWidget(content_frame)

        # Establecer el layout principal del widget
        self.setLayout(accordion_layout)

    def select_directory(self, input_field):
        """
        Abre un QFileDialog para seleccionar un directorio y muestra la ruta en el campo de entrada.
        """
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar directorio")
        if directory:
            input_field.setText(directory)
