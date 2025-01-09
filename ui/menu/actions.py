from libs.comparator import comparator
from libs.normalizer import normalizer
from ui.preferences.pref_window import PreferencesWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

preferences_window_instance = None

def normalizar(window):
    """
    Abre la ventana de procesamiento de Excel como subventana MDI.
    """
    normalizer.normalize(window)

def comparar(window):
    """
    Abre la ventana de comparación de listas como subventana MDI.
    """
    comparator.comparate(window)

def open_preferences(window):
    """
    Abre la ventana de preferencias como una subventana independiente.
    """
    global preferences_window_instance

    if preferences_window_instance is None or not preferences_window_instance.isVisible():
        preferences_window_instance = PreferencesWindow()
        preferences_window_instance.setWindowModality(Qt.ApplicationModal)
        preferences_window_instance.show()

def salir():
    """
    Cierra la aplicación después de confirmar con el usuario.
    """
    respuesta = QMessageBox.question(
        None,
        "Salir",
        "¿Estás seguro de que deseas salir?",
        QMessageBox.Yes | QMessageBox.No
    )
    if respuesta == QMessageBox.Yes:
        exit()
