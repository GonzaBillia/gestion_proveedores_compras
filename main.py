from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from ui.main_window import MainWindow

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Función para manejar excepciones no capturadas.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Permitir que Ctrl+C cierre la aplicación
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # Mostrar un mensaje de error en un cuadro de diálogo
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error")
    error_dialog.setText("Ocurrió un error inesperado:")
    error_dialog.setInformativeText(str(exc_value))
    error_dialog.exec_()

# Redirigir el manejador de excepciones global
sys.excepthook = global_exception_handler

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
