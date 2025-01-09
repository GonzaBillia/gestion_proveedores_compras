from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QSpacerItem, QSizePolicy
)
from ui.preferences.sections.directories_section import DirectoriesSection
from controllers.preferences_controller import PreferencesController
from ui.common.message_box import MessageBox

class PreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferencias")
        self.resize(600, 400)
        self.controller = PreferencesController()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        content_frame = QFrame()
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        self.section_list = QListWidget()
        self.section_list.addItem("Directorios")
        self.section_list.currentRowChanged.connect(self.display_section)

        self.stack = QStackedWidget()
        self.directories_section = DirectoriesSection()
        self.stack.addWidget(self.directories_section)

        content_layout.addWidget(self.section_list, 1)
        content_layout.addWidget(self.stack, 3)

        main_layout.addWidget(content_frame)

        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        button_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        cancel_button = QPushButton("Cancelar")
        cancel_button.setFixedHeight(30)
        cancel_button.clicked.connect(self.close)

        save_button = QPushButton("Guardar")
        save_button.setFixedHeight(30)
        save_button.clicked.connect(self.save_preferences)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        main_layout.addWidget(button_frame)

        self.section_list.setCurrentRow(0)

    def display_section(self, index):
        if index >= 0:
            self.stack.setCurrentIndex(index)
            self.section_list.setCurrentRow(index)

    def save_preferences(self):
        preferences = {}
        for i in range(self.stack.count()):
            widget = self.stack.widget(i)
            if hasattr(widget, "collect_data"):
                preferences.update(widget.collect_data())

        try:
            self.controller.save_preferences(preferences)
            MessageBox.show_info("Preferencias", "Los cambios se guardaron correctamente.")
            print("Preferencias guardadas.")
            self.close()
        except Exception as e:
            MessageBox.show_error("Ocurrio un Error al guardar los datos", f"{e}")
