from libs.comparator import comparator
from libs.normalizer import normalizer
from PyQt5.QtWidgets import QMessageBox

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
