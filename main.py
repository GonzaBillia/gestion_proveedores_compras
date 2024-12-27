import tkinter as tk
from ui.main_window import MainWindow

def main():
    # Crear la raíz de la aplicación
    root = tk.Tk()
    root.title("Gestion de Compras")
    root.geometry("800x600")  # Ancho x Alto

    # Crear la ventana principal
    app = MainWindow(root)

    # Ejecutar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
