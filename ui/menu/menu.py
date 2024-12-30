from PyQt5.QtWidgets import QMainWindow, QAction
from ui.menu.actions import normalizar, comparar, salir

def configure_menu(window: QMainWindow):
    """
    Configura el menú de la ventana principal.
    :param window: Instancia de QMainWindow
    """
    # Crear la barra de menú
    menu_bar = window.menuBar()

    # Crear el menú "Procesos"
    menu_procesos = menu_bar.addMenu("Procesos")

    # Opción "Normalizar"
    normalizar_action = QAction("Normalizar", window)
    normalizar_action.triggered.connect(lambda: normalizar(window))  # Sin paréntesis
    menu_procesos.addAction(normalizar_action)

    # Opción "Comparar"
    comparar_action = QAction("Comparar con Base de Datos", window)
    comparar_action.triggered.connect(comparar)  # Sin paréntesis
    menu_procesos.addAction(comparar_action)

    # Separador
    menu_procesos.addSeparator()

    # Opción "Salir"
    salir_action = QAction("Salir", window)
    salir_action.triggered.connect(salir)  # Sin paréntesis
    menu_procesos.addAction(salir_action)
