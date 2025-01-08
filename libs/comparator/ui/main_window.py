from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QMessageBox, QProgressBar, QHBoxLayout, QWidget, QInputDialog
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

        # Variables
        self.tasks = [
            "Traer Productos desde la Base de Datos",
            "Limpiando resultados",
            "Comparando con lista recibida",
            "Ordenando lista de Productos",
            "Guardando Archivos Procesados",
            "Comparando por Proveedor",
            "Guardando Resultado",
            "Generando Reportes",
            "Guardando Archivos"
        ]
        self.task_widgets = []
        self.worker_thread = None

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Título
        self.label = QLabel("Progreso de Tareas", self)
        self.label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        # Contenedor de tareas
        self.task_layout = QVBoxLayout()
        self.layout.addLayout(self.task_layout)

        for task_name in self.tasks:
            task_widget = QWidget()
            task_layout = QHBoxLayout(task_widget)

            # Reducir los márgenes
            task_layout.setContentsMargins(0, 5, 0, 5)  # Márgenes más pequeños
            task_layout.setSpacing(5)

            # Tarea
            task_label = QLabel(task_name, self)
            task_label.setStyleSheet("font-size: 14px;")  # Ajustar tamaño de fuente
            task_layout.addWidget(task_label)

            # Spinner
            spinner = Spinner()
            spinner.setFixedSize(20, 20)  # Ajustar tamaño del spinner
            spinner.hide()  # Ocultar inicialmente
            task_layout.addWidget(spinner)

            # Alinear los widgets en el centro
            task_layout.setAlignment(Qt.AlignVCenter)

            self.task_widgets.append((task_label, spinner))
            self.task_layout.addWidget(task_widget)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(self.tasks))
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Botón para seleccionar archivo
        self.start_button = QPushButton("Seleccionar Archivo y Procesar", self)
        self.start_button.clicked.connect(self.load_and_start_tasks)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

    def load_and_start_tasks(self):
        file_path, nombre_proveedor = self.pedir_ubicacion_archivo()
        if not file_path:
            QMessageBox.warning(self, "Advertencia", "No se seleccionó ningún archivo.")
            return

        # Deshabilitar el botón y mostrar progreso
        self.start_button.setDisabled(True)
        self.start_tasks(file_path, nombre_proveedor)

    def start_tasks(self, provider_df_path, provider_name):
        # Configurar el hilo de trabajo
        self.worker_thread = WorkerThread()
        self.worker_thread.provider_df = provider_df_path
        self.worker_thread.provider_name = provider_name
        self.worker_thread.task_completed.connect(self.update_task_ui)
        self.worker_thread.all_tasks_completed.connect(self.complete_all_tasks)
        self.worker_thread.start()

        # Iniciar la primera tarea
        self.update_task_ui(0)

    def update_task_ui(self, task_index):
        if task_index < len(self.task_widgets):
            # Actualizar spinner y barra de progreso
            task_label, spinner = self.task_widgets[task_index]
            spinner.show()
            self.progress_bar.setValue(task_index + 1)

            # Ocultar spinner de la tarea previa
            if task_index > 0:
                prev_task_label, prev_spinner = self.task_widgets[task_index - 1]
                prev_spinner.hide()
                prev_task_label.setDisabled(True)

    def complete_all_tasks(self, task_index):
        task_label, spinner = self.task_widgets[task_index]
        task_label.setDisabled(True)
        spinner.hide()
        QMessageBox.information(self, "Completado", "Todas las tareas han finalizado.")

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
        # Pedir el nombre del proveedor
        nombre_proveedor, ok = QInputDialog.getText(self, "Nombre del Proveedor", "Ingrese el nombre del proveedor:")
        
        if not ok or not nombre_proveedor:
            QMessageBox.warning(self, "Advertencia", "No se ingresó ningún nombre de proveedor.")
            return None, None


        # Retornar ambos valores
        return file_path, nombre_proveedor
