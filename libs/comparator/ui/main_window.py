from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from functools import partial
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QMessageBox, QProgressBar, QHBoxLayout, QWidget, QInputDialog, QSizePolicy, QSpacerItem
)
from libs.comparator.ui.threads.worker_thread import WorkerThread
from libs.comparator.ui.components.spinner import Spinner

class ListComparator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mantenimiento de Base de Datos")
        self.setGeometry(100, 100, 600, 500)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop)

        # Variables
        self.tasks = {
            "Comparando Datos": [
                "Traer Productos desde la Base de Datos",
                "Limpiando resultados",
                "Comparando con lista recibida",
                "Ordenando lista de Productos",
                "Guardando Archivos Procesados",
                "Comparando por Proveedor",
                "Guardando Resultados",
                "Proceso Completado"
            ],
            "Generando Reportes": [
                "Ordenando Reportes",
                "Guardando Archivos",
                "Proceso Completado"
            ]
        }

        self.task_widgets = []
        self.current_task_index = 0
        self.current_subtask_index = 0
        self.worker_thread = None


        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Título
        self.label = QLabel("Proceso de Comparación y Reporting", self)
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px 0px;")
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        # Ajustar los márgenes del layout
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(20)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignTop)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.get_total_subtasks())
        self.progress_bar.setValue(0)
        progress_layout = QVBoxLayout()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.layout.addLayout(progress_layout)

        # Contenedor de tareas
        self.task_layout = QVBoxLayout()
        self.task_layout.setContentsMargins(0, 5, 0, 5)  # Ajustar márgenes
        self.task_layout.setSpacing(20)  # Ajustar espaciado
        self.layout.addLayout(self.task_layout)

        for task_name, subtasks in self.tasks.items():
            spinner = Spinner()
            spinner.setFixedSize(20, 20)
            spinner.hide()

            # Título de la tarea principal
            task_label = QLabel(task_name, self)
            task_label.setStyleSheet("font-size: 12px; font-weight: bold; margin: 10px 0 5px 0; width: auto;")
            task_label.setAlignment(Qt.AlignLeft)
            task_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # Spinner
            spinner = Spinner()
            spinner.setFixedSize(20, 20)
            spinner.hide()

            # Layout del título y spinner
            task_widget = QWidget()
            task_layout = QHBoxLayout(task_widget)
            task_layout.setContentsMargins(0, 0, 0, 0)
            task_layout.setSpacing(10)
            task_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            task_layout.addWidget(task_label)
            task_layout.addWidget(spinner)

            task_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.task_layout.addWidget(task_widget)

            # Contenedor para la subtarea actual
            subtask_widget = QWidget()
            subtask_layout = QHBoxLayout(subtask_widget)
            subtask_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            # Label de la subtarea
            subtask_label = QLabel("", self)
            subtask_label.setStyleSheet("font-size: 11px; margin-left: 15px;")
            subtask_layout.addWidget(subtask_label)

            subtask_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            subtask_layout.setContentsMargins(15, 2, 0, 2)  # Reduce los márgenes de la subtask
            subtask_layout.setSpacing(5)  # Espaciado más pequeño entre elementos de la subtask
            subtask_widget.hide()  # Ocultar inicialmente

            self.task_widgets.append((task_label, subtask_label, spinner, subtask_widget, subtasks))
            self.task_layout.addWidget(subtask_widget)

        # Espaciador flexible para mantener los widgets alineados arriba
        spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        # Botón para seleccionar archivo
        self.start_button = QPushButton("Seleccionar Archivo y Procesar", self)
        self.start_button.setFixedHeight(30)
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_button.clicked.connect(self.load_and_start_tasks)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignBottom)

    def get_total_subtasks(self):
        return sum(len(subtasks) for subtasks in self.tasks.values())

    def load_and_start_tasks(self):
        file_path = self.pedir_ubicacion_archivo()
        if not file_path:
            QMessageBox.warning(self, "Advertencia", "No se seleccionó ningún archivo.")
            return

        # Deshabilitar el botón y mostrar progreso
        self.start_button.setDisabled(True)
        self.start_tasks(file_path)

    def start_tasks(self, provider_df_path):
        # Configurar el hilo de trabajo
        self.worker_thread = WorkerThread()
        # Conectar señales
        self.worker_thread.request_filename.connect(self.show_filename_dialog)
        self.worker_thread.filename_provided.connect(self.worker_thread.set_filename)
        self.worker_thread.request_save_file_path.connect(self.show_save_file_dialog)
        self.worker_thread.file_path_provided.connect(self.worker_thread.set_file_path)
        self.worker_thread.task_completed.connect(partial(self.update_task_ui))
        self.worker_thread.all_tasks_completed.connect(self.complete_all_tasks)
        self.worker_thread.error_occurred.connect(self.show_error_message)  # <<--- AQUÍ
        self.worker_thread.provider_df = provider_df_path

        self.worker_thread.start()
        self.update_task_ui(0, 0)

    def update_task_ui(self, task_index, subtask_index):
        if task_index < len(self.task_widgets):
            task_label, subtask_label, spinner, subtask_widget, subtasks = self.task_widgets[task_index]

            # Mostrar la subtarea actual
            subtask_label.setText(subtasks[subtask_index])
            subtask_widget.show()
            
            # Mostrar el spinner solo en el título de la tarea
            if subtask_index == 0:
                spinner.show()

            # Actualizar barra de progreso
            total_subtasks = self.get_total_subtasks()
            completed_subtasks = sum(len(self.tasks[task]) for task in list(self.tasks.keys())[:task_index]) + subtask_index + 1
            self.progress_bar.setValue(completed_subtasks)

            # Avanzar al siguiente subtask o task
            self.current_subtask_index = subtask_index + 1
            if self.current_subtask_index >= len(subtasks):
                spinner.hide()
                self.current_subtask_index = 0
                self.current_task_index += 1
                if self.current_task_index < len(self.task_widgets):
                    self.update_task_ui(self.current_task_index, 0)

    def complete_all_tasks(self):
        QMessageBox.information(self, "Completado", "Todas las tareas han finalizado.")
        self.start_button.setDisabled(False)

    def show_error_message(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.start_button.setDisabled(False)
        
    def pedir_ubicacion_archivo(self):
        # Abrir el diálogo para seleccionar el archivo
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos soportados (*.xlsx *.csv *.pdf *.txt);;Archivos de Excel (*.xlsx);;Archivos CSV (*.csv);;Archivos PDF (*.pdf);;Archivos de texto (*.txt)",
            options=options,
        )

        # Retornar ambos valores
        return file_path

    def show_filename_dialog(self, type):
        filename, ok = QInputDialog.getText(None, "Guardar archivo", f"Ingrese el nombre del archivo {type}:")
        if filename and ok:
            self.worker_thread.filename_provided.emit(filename)
        else:
            self.worker_thread.filename_provided.emit("")
    
    def show_save_file_dialog(self):
        """
        Muestra un cuadro de diálogo para que el usuario seleccione la ruta del archivo.
        """
        full_path, _ = QFileDialog.getSaveFileName(self, f"Guardar archivo", "", "Excel files (*.xlsx)")
        if full_path:
            self.worker_thread.file_path_provided.emit(full_path)
        else:
            self.worker_thread.file_path_provided.emit("")