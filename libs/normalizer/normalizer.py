import sys
from PyQt5.QtCore import Qt  # Importar Qt para el tipo de ventana
from libs.normalizer.ui.ui import ExcelProcessorApp

def normalize(parent_window):
    """
    Lanza la ventana de ExcelProcessorApp como una subventana.
    :param parent_window: Instancia de QMainWindow principal.
    """
    window = ExcelProcessorApp()
    window.setParent(parent_window)  # Asegurar que sea una subventana
    window.show()