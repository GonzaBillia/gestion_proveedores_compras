from PyQt5.QtCore import QThread, pyqtSignal
from libs.comparator.controllers.process_controller import make_comparation

class WorkerThread(QThread):
    task_completed = pyqtSignal(int)  # Señal para notificar que una tarea se completó
    all_tasks_completed = pyqtSignal()  # Señal para notificar que todas las tareas se completaron
    provider_df = None  # Datos del proveedor cargados

    def run(self):
        """
        Ejecuta el proceso de comparación en un hilo secundario y emite señales al hilo principal.
        """
        try:
            make_comparation(self.provider_df, self.emit_update_ui_signal)
        except Exception as e:
            print(f"Error en WorkerThread: {e}")
        self.all_tasks_completed.emit()  # Notificar que todas las tareas se completaron

    def emit_update_ui_signal(self, task_index):
        """
        Método para emitir una señal cuando se completa una tarea específica.

        :param task_index: Índice de la tarea completada.
        """
        self.task_completed.emit(task_index)
