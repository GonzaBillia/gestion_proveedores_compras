from PyQt5.QtWidgets import QMainWindow, QAction, QMdiSubWindow
from PyQt5.QtCore import Qt
from ui.menu.actions import normalizar, comparar, salir

def configure_menu(window: QMainWindow):
    menu_bar = window.menuBar()

    # Crear el menú "Procesos"
    menu_procesos = menu_bar.addMenu("Procesos")

    # Opción "Normalizar"
    normalizar_action = QAction("Normalizar", window)
    normalizar_action.triggered.connect(lambda: load_widget(window, normalizar))
    menu_procesos.addAction(normalizar_action)

    # Opción "Comparar"
    comparar_action = QAction("Comparar con Base de Datos", window)
    comparar_action.triggered.connect(lambda: load_widget(window, comparar))
    menu_procesos.addAction(comparar_action)

    # Separador
    menu_procesos.addSeparator()

    # Opción "Salir"
    salir_action = QAction("Salir", window)
    salir_action.triggered.connect(salir)
    menu_procesos.addAction(salir_action)

def load_widget(window: QMainWindow, widget_function):
    """
    Agrega un nuevo widget como una subventana dentro del área MDI.
    """
    # Crear el nuevo widget usando la función proporcionada
    widget = widget_function(window)

    # Crear una subventana MDI
    sub_window = QMdiSubWindow()
    sub_window.setWidget(widget)
    sub_window.setAttribute(Qt.WA_DeleteOnClose)

    # Agregar la subventana al área MDI
    window.mdi_area.addSubWindow(sub_window)
    sub_window.show()
