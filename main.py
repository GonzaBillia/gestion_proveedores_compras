from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Crear la aplicación
    app = QApplication([])

    # Crear la ventana principal
    window = MainWindow()
    window.setWindowTitle("Gestión de Compras")
    window.setGeometry(100, 100, 800, 600)  # X, Y, Ancho, Alto

    # Mostrar la ventana
    window.show()

    # Ejecutar la aplicación
    app.exec_()

if __name__ == "__main__":
    main()
