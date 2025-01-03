from PyQt5.QtWidgets import QMainWindow, QMdiArea
from ui.menu.menu import configure_menu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con Menú")
        self.setGeometry(100, 100, 800, 600)

        # Crear el área MDI
        self.mdi_area = QMdiArea()  # Asegúrate de que el nombre es mdi_area
        self.setCentralWidget(self.mdi_area)

        # Configurar el menú principal
        configure_menu(self)
