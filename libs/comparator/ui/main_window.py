from PyQt5.QtWidgets import QFileDialog

def pedir_ubicacion_archivo(parent=None):
    """
    Muestra un diálogo para que el usuario seleccione un archivo y retorna su ruta.
    
    :param parent: Ventana principal (opcional, puede ser None).
    :return: La ruta completa del archivo seleccionado o None si el usuario cancela.
    """
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly  # Abrir en modo solo lectura (opcional)
    
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Seleccionar archivo",  # Título del diálogo
        "",                     # Directorio inicial (vacío para usar el predeterminado)
        "Archivos soportados (*.xlsx *.csv *.pdf *.txt);;Archivos de Excel (*.xlsx);;Archivos CSV (*.csv);;Archivos PDF (*.pdf);;Archivos de texto (*.txt)",  # Filtros
        options=options
    )
    
    return file_path if file_path else None
