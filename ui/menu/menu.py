from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox

def nuevo_proceso():
    # Función para manejar la acción "Nuevo Proceso"
    QMessageBox.information(None, "Nuevo Proceso", "Aquí se iniciará un nuevo proceso.")

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

def configure_menu(window: QMainWindow):
    """
    Configura el menú de la ventana principal.
    :param window: Instancia de QMainWindow
    """
    # Crear la barra de menú
    menu_bar = window.menuBar()

    # Crear el menú "Procesos"
    menu_procesos = menu_bar.addMenu("Procesos")

    # Opción "Nuevo Proceso"
    nuevo_proceso_action = QAction("Nuevo Proceso", window)
    nuevo_proceso_action.triggered.connect(nuevo_proceso)
    menu_procesos.addAction(nuevo_proceso_action)

    # Separador
    menu_procesos.addSeparator()

    # Opción "Salir"
    salir_action = QAction("Salir", window)
    salir_action.triggered.connect(salir)
    menu_procesos.addAction(salir_action)
