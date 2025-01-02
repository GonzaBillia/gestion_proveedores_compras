from PyQt5.QtWidgets import QFileDialog, QInputDialog

def pedir_ubicacion_archivo(parent=None):
    """
    Muestra un diálogo para que el usuario seleccione un archivo y retorna su ruta.
    
    :param parent: Ventana principal (opcional, puede ser None).
    :return: La ruta completa del archivo seleccionado o None si el usuario cancela.
    """
    # Diálogo para seleccionar la ubicación del archivo
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Seleccionar archivo",
        "",
        "Archivos soportados (*.xlsx *.csv *.pdf *.txt);;Archivos de Excel (*.xlsx);;Archivos CSV (*.csv);;Archivos PDF (*.pdf);;Archivos de texto (*.txt)",
        options=options
    )

    if not file_path:
        # Si el usuario cancela la selección del archivo
        return None, None

    # Diálogo para ingresar el nombre del archivo
    name, ok = QInputDialog.getText(
        parent,
        "Ingresar nombre del proveedor con el que se guardara el archivo",
        "Nombre del proveedor:"
    )

    if not ok or not name.strip():
        # Si el usuario cancela o no ingresa un nombre válido
        return None, None

    # Retornar la ruta seleccionada y el nombre ingresado
    return file_path, name.strip()
