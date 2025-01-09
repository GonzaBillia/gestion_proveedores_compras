from PyQt5.QtWidgets import QMessageBox


class MessageBox:
    @staticmethod
    def show_info(title, message):
        """
        Muestra un MessageBox de información.
        :param title: El título del mensaje.
        :param message: El contenido del mensaje.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    @staticmethod
    def show_warning(title, message):
        """
        Muestra un MessageBox de advertencia.
        :param title: El título del mensaje.
        :param message: El contenido del mensaje.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    @staticmethod
    def show_error(title, message):
        """
        Muestra un MessageBox de error.
        :param title: El título del mensaje.
        :param message: El contenido del mensaje.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    @staticmethod
    def show_confirmation(title, message):
        """
        Muestra un MessageBox de confirmación.
        :param title: El título del mensaje.
        :param message: El contenido del mensaje.
        :return: True si el usuario selecciona 'Sí', False si selecciona 'No'.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        return result == QMessageBox.Yes
