from PyQt5.QtCore import QThread, pyqtSignal
from libs.comparator.controllers.process_controller import make_comparation, make_provider_comparation,setup_report, make_report

class WorkerThread(QThread):
    task_completed = pyqtSignal(int)  # Señal para notificar que una tarea se completó
    all_tasks_completed = pyqtSignal(int)  # Señal para notificar que todas las tareas se completaron
    provider_df = None  # Datos del proveedor cargados
    provider_name = None

    def run(self):
        """
        Ejecuta el proceso de comparación en un hilo secundario y emite señales al hilo principal.
        """
        try:
            unmatched, matches_p, unmatched_cb, cost_df, provider_list = make_comparation(self.provider_df, self.provider_name, self.emit_update_ui_signal)

            quantio_matches_df = make_provider_comparation(matches_p, provider_list, self.provider_name, self.emit_update_ui_signal)

            df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb, cost_df)

            make_report(df_array, self.provider_name, self.emit_update_ui_signal)

            self.all_tasks_completed.emit(len(provider_list))  # Notificar que todas las tareas se completaron
        except Exception as e:
            print(f"Error en WorkerThread: {e}")
        
        

    def emit_update_ui_signal(self, task_index):
        """
        Método para emitir una señal cuando se completa una tarea específica.

        :param task_index: Índice de la tarea completada.
        """
        self.task_completed.emit(task_index)
    