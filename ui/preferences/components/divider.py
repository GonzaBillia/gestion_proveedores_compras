from PyQt5.QtWidgets import QFrame

class Divider(QFrame):
    def __init__(self):
        """
        Componente reutilizable para crear un divisor horizontal.
        """
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("margin: 10px 0;")
