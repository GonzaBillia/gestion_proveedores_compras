from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt, QSize
from libs.normalizer.ui.ui import ExcelProcessorApp

def normalize(parent_window):
    """
    Lanza la ventana de ExcelProcessorApp como una subventana MDI.
    """
    for subwindow in parent_window.mdi_area.subWindowList():
        if isinstance(subwindow.widget(), ExcelProcessorApp):
            subwindow.setFocus()
            return

    # Crear la subventana
    window = ExcelProcessorApp()
    sub_window = QMdiSubWindow()
    sub_window.setWidget(window)
    sub_window.setAttribute(Qt.WA_DeleteOnClose)

    sub_window.setMinimumSize(QSize(300, 200))

    parent_window.mdi_area.addSubWindow(sub_window)
    sub_window.show()
