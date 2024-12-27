import tkinter as tk
from tkinter import messagebox

def nuevo_proceso():
    messagebox.showinfo("Nuevo Proceso", "Aquí se iniciará un nuevo proceso.")

def salir():
    exit()

def configure_menu(root):
    # Crear el menú superior
    menu_bar = tk.Menu(root)

    # Crear la categoría "Procesos"
    menu_procesos = tk.Menu(menu_bar, tearoff=0)
    menu_procesos.add_command(label="Nuevo Proceso", command=nuevo_proceso)
    menu_procesos.add_separator()
    menu_procesos.add_command(label="Salir", command=salir)

    # Agregar la categoría "Procesos" al menú principal
    menu_bar.add_cascade(label="Procesos", menu=menu_procesos)

    # Configurar el menú en la ventana principal
    root.config(menu=menu_bar)
