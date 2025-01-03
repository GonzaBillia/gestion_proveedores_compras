from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from ui.main_window import MainWindow

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error")
    error_dialog.setText("Ocurrió un error inesperado:")
    error_dialog.setInformativeText(str(exc_value))
    error_dialog.exec_()

sys.excepthook = global_exception_handler

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
