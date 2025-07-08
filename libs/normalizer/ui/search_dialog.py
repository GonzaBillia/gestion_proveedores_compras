from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel
)

class SearchSelectDialog(QDialog):
    def __init__(self, fetch_providers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar proveedor")
        self.selected_id = None

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Buscar proveedor:", self)
        self.layout.addWidget(self.label)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar...")
        self.layout.addWidget(self.search_input)

        self.combo = QComboBox(self)
        self.layout.addWidget(self.combo)

        self.ok_button = QPushButton("Aceptar", self)
        self.ok_button.clicked.connect(self.accept_selection)
        self.layout.addWidget(self.ok_button)

        # Traer proveedores y guardar la lista original para el filtrado
        self.providers = fetch_providers()  # Lista de tuplas (id, nombre)
        self.filtered = list(self.providers)
        self.populate_combo(self.filtered)

        self.search_input.textChanged.connect(self.filter_combo)

    def populate_combo(self, items):
        self.combo.clear()
        for prov_id, name in items:
            self.combo.addItem(name, prov_id)

    def filter_combo(self, text):
        text = text.lower()
        self.filtered = [
            (prov_id, name) for prov_id, name in self.providers
            if text in name.lower()
        ]
        self.populate_combo(self.filtered)

    def accept_selection(self):
        index = self.combo.currentIndex()
        if index >= 0:
            self.selected_id = self.combo.itemData(index)
        self.accept()
