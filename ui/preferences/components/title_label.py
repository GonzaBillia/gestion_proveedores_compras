from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class TitleLabel(QLabel):
    def __init__(self, text):
        """
        Componente reutilizable para crear un título de sección.
        
        :param text: El texto que se mostrará como título.
        """
        super().__init__(text)
        self.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.setAlignment(Qt.AlignLeft)
