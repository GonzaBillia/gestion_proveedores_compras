from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt, QSize
from libs.comparator.ui.main_window import ListComparator

def comparate(parent_window):
    """
    Lanza la ventana de ListComparator como una subventana MDI.
    """
    for subwindow in parent_window.mdi_area.subWindowList():
        if isinstance(subwindow.widget(), ListComparator):
            subwindow.setFocus()
            return

    # Crear la subventana
    window = ListComparator()
    sub_window = QMdiSubWindow()
    sub_window.setWidget(window)
    sub_window.setAttribute(Qt.WA_DeleteOnClose)

    sub_window.setMinimumSize(QSize(400, 400))

    parent_window.mdi_area.addSubWindow(sub_window)
    sub_window.show()
