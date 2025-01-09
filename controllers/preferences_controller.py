import os
import json


class PreferencesController:
    def __init__(self):
        """
        Inicializa el controlador de preferencias, creando las carpetas y archivos necesarios.
        """
        self.base_path = os.path.join(os.path.expanduser("~"), "Documents", "Gestor_compras")
        self.files_path = os.path.join(self.base_path, "files")
        self.config_path = os.path.join(self.base_path, "config")
        self.directories_file = os.path.join(self.config_path, "directories.json")

        # Crear las carpetas necesarias
        self._ensure_directories_exist()
        self._ensure_preferences_file()

    def _ensure_directories_exist(self):
        """
        Crea las carpetas necesarias si no existen.
        """
        directories_to_create = [
            self.base_path,
            self.config_path,
            os.path.join(self.base_path, "files", "normalizados"),
            os.path.join(self.base_path, "files", "comparados"),
            os.path.join(self.base_path, "files", "reportes"),
        ]

        for directory in directories_to_create:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Carpeta creada: {directory}")

    def _ensure_preferences_file(self):
        """
        Crea el archivo de preferencias si no existe.
        """
        if not os.path.exists(self.directories_file):
            default_preferences = {
                "directories": {
                    "normalized_file_dir": os.path.join(self.base_path, "files", "normalizados"),
                    "comparator_processed_file_dir": os.path.join(self.base_path, "files", "comparados"),
                    "reports_dir": os.path.join(self.base_path, "files", "reportes")
                }
            }
            with open(self.directories_file, "w") as file:
                json.dump(default_preferences, file, indent=4)
            print(f"Archivo de preferencias creado: {self.directories_file}")

    def load_preferences(self):
        """
        Carga las preferencias desde el archivo JSON.
        :return: Un diccionario con las preferencias.
        """
        if os.path.exists(self.directories_file):
            with open(self.directories_file, "r") as file:
                preferences = json.load(file)
            return preferences
        return {}

    def save_preferences(self, preferences):
        """
        Guarda las preferencias en el archivo JSON.
        :param preferences: Un diccionario con las preferencias a guardar.
        """
        with open(self.directories_file, "w") as file:
            json.dump(preferences, file, indent=4)
        print("Preferencias guardadas correctamente.")
