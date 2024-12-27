from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.menu.menu import configure_menu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con Menú")
        self.setGeometry(100, 100, 400, 300)
        
        # Configurar el menú principal
        configure_menu(self)