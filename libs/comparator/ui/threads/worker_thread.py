from PyQt5.QtCore import QThread, pyqtSignal
from libs.comparator.controllers.process_controller import make_comparation

class WorkerThread(QThread):
    task_completed = pyqtSignal(int)  # Señal para notificar que una tarea se completó
    all_tasks_completed = pyqtSignal()  # Señal para notificar que todas las tareas se completaron
    provider_df = None  # Datos del proveedor cargados

    def update_ui_callback(self, task_index):
        """
        Método para emitir una señal cuando se completa una tarea específica.

        :param task_index: Índice de la tarea completada.
        """
        self.task_completed.emit(task_index)

    def run(self):
        # Ejecutar el proceso y emitir señales para cada tarea
        make_comparation(self.provider_df, self.update_ui_callback)
        self.all_tasks_completed.emit()  # Notificar que todas las tareas se completaron
