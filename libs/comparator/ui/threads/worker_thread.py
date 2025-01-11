from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop
from libs.comparator.controllers.process_controller import make_comparation, make_provider_comparation,setup_report
from libs.comparator.services.reports import reports
from functools import partial

class WorkerThread(QThread):
    task_completed = pyqtSignal(int, int)  # Señal para notificar que una tarea se completó
    all_tasks_completed = pyqtSignal()  # Señal para notificar que todas las tareas se completaron
    request_filename = pyqtSignal(str)
    filename_provided = pyqtSignal(str)
    request_save_file_path = pyqtSignal()
    file_path_provided = pyqtSignal(str)
    provider_df = None  # Datos del proveedor cargados

    def run(self):
        """
        Ejecuta el proceso de comparación en un hilo secundario y emite señales al hilo principal.
        """
        try:
            unmatched, matches_p, unmatched_cb, cost_df, provider_list, file_name = make_comparation(self.provider_df, self.emit_update_ui_signal)

            quantio_matches_df = make_provider_comparation(matches_p, provider_list, self.emit_update_ui_signal, file_name)
            self.emit_update_ui_signal(0, 7)

            df_array = setup_report(unmatched, quantio_matches_df, unmatched_cb, cost_df)

            # Crea funciones parciales con el argumento predefinido
            req_filename_reporte = partial(self.thread_req_filename, "Reporte")
            req_filename_costos = partial(self.thread_req_filename, "Costos")

            reports.make_report(df_array, self.emit_update_ui_signal, req_filename_reporte, req_filename_costos, self.thread_req_save_file_path)
            self.emit_update_ui_signal(1, 2)
            self.all_tasks_completed.emit()  # Notificar que todas las tareas se completaron
        except Exception as e:
            print(f"Error en WorkerThread: {e}")
        
        

    def emit_update_ui_signal(self, task_index, subtask_index):
        """
        Método para emitir una señal cuando se completa una tarea específica.

        :param task_index: Índice de la tarea completada.
        """
        self.task_completed.emit(task_index, subtask_index)
    

    def thread_req_filename(self, type):
        """
        Función para solicitar el nombre del archivo al hilo principal.
        """
        self.request_filename.emit(type)

        # Esperar hasta recibir la respuesta
        loop = QEventLoop()
        self.filename_provided.connect(loop.quit)
        loop.exec_()

        filename = self.filename

        # Verificar si se proporcionó un nombre de archivo
        if not filename:
            raise Exception("No se proporcionó un nombre de archivo.")
        
        return filename
    
    def set_filename(self, filename):
        self.filename = filename


    def thread_req_save_file_path(self):
        """
        Función para solicitar la ruta del archivo al hilo principal.
        """
        self.request_save_file_path.emit()

        # Esperar hasta recibir la respuesta
        loop = QEventLoop()
        self.file_path_provided.connect(loop.quit)
        loop.exec_()

        return self.file_path

    def set_file_path(self, path):
        self.file_path = path