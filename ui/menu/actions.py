from libs.comparator import comparator
from libs.normalizer import normalizer
from PyQt5.QtWidgets import QMessageBox

def normalizar(window):
    normalizer.normalize(window)

def comparar(window):
    # Función para manejar la acción "Nuevo Proceso"s
    comparator.comparate(window)

def salir():
    # Función para manejar la acción "Salir"
    respuesta = QMessageBox.question(
        None,
        "Salir",
        "¿Estás seguro de que deseas salir?",
        QMessageBox.Yes | QMessageBox.No
    )
    if respuesta == QMessageBox.Yes:
        exit()