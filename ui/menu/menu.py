from PyQt5.QtWidgets import QMainWindow, QAction, QMdiSubWindow
from PyQt5.QtCore import Qt
from ui.menu.actions import normalizar, comparar, open_preferences, salir

def configure_menu(window: QMainWindow):
    menu_bar = window.menuBar()

    # Crear el menú "Procesos"
    menu_procesos = menu_bar.addMenu("Archivo")
    menu_config = menu_bar.addMenu("Configuración")

    # Opción "Normalizar"
    normalizar_action = QAction("Normalizar", window)
    normalizar_action.triggered.connect(lambda: normalizar(window))
    menu_procesos.addAction(normalizar_action)

    # Opción "Comparar"
    comparar_action = QAction("Comparar con Base de Datos", window)
    comparar_action.triggered.connect(lambda: comparar(window))
    menu_procesos.addAction(comparar_action)

    pref_action = QAction("Preferencias", window)
    pref_action.triggered.connect(lambda: open_preferences(window))
    menu_config.addAction(pref_action)

    # Separador
    menu_procesos.addSeparator()

    # Opción "Salir"
    salir_action = QAction("Salir", window)
    salir_action.triggered.connect(salir)
    menu_procesos.addAction(salir_action)

