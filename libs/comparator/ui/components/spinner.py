from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
import sys

class Spinner(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)  # Velocidad de giro
        self.resize(24, 24)  # Tamaño del spinner

    def rotate(self):
        self.angle += 30
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        for i in range(12):
            painter.setBrush(Qt.black if i % 3 == 0 else Qt.gray)
            painter.drawEllipse(-2, -8, 4, 4)
            painter.rotate(30)