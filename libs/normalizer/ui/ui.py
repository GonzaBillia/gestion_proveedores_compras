import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox, ttk
from libs.normalizer.controllers.file_controller import FileController
from libs.normalizer.services.data_processor import DataProcessor


class ExcelProcessorApp:
    def __init__(self, root):
        """
        Inicializa la aplicación principal.
        :param root: Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Excel Processor")
        self.root.geometry("900x500")
        self.root.configure(bg="#e0e0e0")

        # Instancias de lógica separada
        self.file_manager = FileController()
        self.data_processor = DataProcessor()

        # Configuración de estilos
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10, foreground="white", background="#007bff")
        style.map("TButton", background=[("active", "#0056b3"), ("!disabled", "#007bff")])

        # Variables de la interfaz
        self.process_by_sheets = tk.BooleanVar()

        # Crear los elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        """
        Crea los elementos de la interfaz.
        """
        tk.Label(self.root, text="Escoge una o más opciones", font=("Arial", 16), bg="#e0e0e0").pack(pady=10)
        ttk.Checkbutton(self.root, text="Procesar por hojas", variable=self.process_by_sheets).pack(pady=5)
        ttk.Button(self.root, text="Subir archivos", command=self.upload_and_list_files).pack(pady=20)

    def upload_and_list_files(self):
        """
        Muestra un cuadro de diálogo para seleccionar archivos Excel.
        """
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_paths:
            return

        self.file_manager.load_files(file_paths)

        if self.process_by_sheets.get():
            self.show_sheet_selection()
        else:
            self.process_next_file()

    def show_sheet_selection(self):
        """
        Crea una ventana para seleccionar hojas de los archivos cargados.
        """
        for file in self.file_manager.file_names:
            sheet_names = self.file_manager.get_sheet_names(file)
            sheet_selection_window = tk.Toplevel(self.root)
            sheet_selection_window.configure(bg="#e0e0e0")
            sheet_selection_window.title(f"Selecciona hojas para {file}")

            sheet_checkboxes = [tk.BooleanVar() for _ in sheet_names]
            for var, sheet in zip(sheet_checkboxes, sheet_names):
                ttk.Checkbutton(sheet_selection_window, text=sheet, variable=var).pack(anchor='w', padx=10, pady=5)

            ttk.Button(
                sheet_selection_window,
                text="Procesar hojas seleccionadas",
                command=lambda: self.set_sheet_selection(file, sheet_checkboxes, sheet_names, sheet_selection_window)
            ).pack(pady=10)

    def set_sheet_selection(self, file, checkboxes, sheet_names, window):
        """
        Establece las hojas seleccionadas para un archivo.
        """
        selected_sheets = [sheet for var, sheet in zip(checkboxes, sheet_names) if var.get()]
        self.file_manager.set_sheet_selection(file, selected_sheets)
        window.destroy()
        self.process_next_file()

    def process_next_file(self):
        """
        Procesa el siguiente archivo en la lista.
        """
        try:
            # Si existe un contenedor anterior, destrúyelo
            if hasattr(self, 'current_file_frame') and self.current_file_frame:
                self.current_file_frame.destroy()

            file_generator = self.file_manager.get_next_file()
            file, sheet = next(file_generator)

            self.current_sheet_name = sheet
            self.header_line = tk.IntVar(value=1)  # Inicializar `header_line` aquí

            # Crear un contenedor para los widgets del archivo actual
            self.current_file_frame = tk.Frame(self.root, bg="#e0e0e0")
            self.current_file_frame.pack(pady=10, fill=tk.BOTH)

            header_line_label = tk.Label(
                self.current_file_frame,
                text=f"Línea de encabezado para {file} - Hoja: {sheet if sheet else 'Completa'}:",
                bg="#e0e0e0"
            )
            header_line_label.pack()

            header_line_entry = tk.Entry(self.current_file_frame, textvariable=self.header_line)
            header_line_entry.pack()

            button_read_header = ttk.Button(
                self.current_file_frame,
                text=f"Leer encabezados de {file} - Hoja: {sheet if sheet else 'Completa'}",
                command=lambda: self.read_header(file, sheet)
            )
            button_read_header.pack(pady=10)
        except StopIteration:
            # Mostrar opciones finales cuando no hay más archivos
            self.show_final_options()
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el siguiente archivo: {str(e)}")


    def read_header(self, file_name, sheet_name):
        """
        Lee el encabezado del archivo y muestra las columnas en una ventana.
        """
        header_row = self.header_line.get() - 1
        df = self.file_manager.read_excel(file_name, sheet_name, header_row)
        if isinstance(df, pd.DataFrame):  # Verificar que sea un DataFrame
            if df.empty:
                messagebox.showerror("Error", f"El archivo {file_name} (Hoja: {sheet_name}) está vacío.")
                return
            self.data_processor.df = df
            self.create_columns_window(file_name, sheet_name)
        else:
            messagebox.showerror("Error", "Error al leer el archivo. Por favor, verifica el archivo seleccionado.")


    def create_columns_window(self, file_name, sheet_name):
        """
        Crea una ventana para mostrar y seleccionar columnas del archivo.
        """
        columns_window = tk.Toplevel(self.root)
        columns_window.geometry("900x400")
        columns_window.configure(bg="#e0e0e0")
        columns_window.title(f"Cabeceras del archivo {file_name} - Hoja: {sheet_name}")

        frame_canvas = tk.Frame(columns_window)
        frame_canvas.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame_canvas, bg="#e0e0e0")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill="y")

        frame_scrollable = tk.Frame(canvas, bg="#e0e0e0")
        canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_scrollable.bind("<Configure>", on_frame_configure)

        self.checkboxes = []
        self.order_inputs = []

        for row, col in enumerate(self.data_processor.df.columns, start=1):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(frame_scrollable, text=col, variable=var)
            cb.grid(row=row, column=0, sticky="w", padx=3, pady=3)
            self.checkboxes.append(var)

            order_var = tk.IntVar(value=0)
            order_entry = tk.Entry(frame_scrollable, textvariable=order_var, width=5)
            order_entry.grid(row=row, column=1, padx=5, pady=3)
            self.order_inputs.append(order_var)

        ttk.Button(
            frame_scrollable,
            text="Agregar columnas seleccionadas",
            command=lambda: self.select_columns(columns_window)
        ).grid(row=row + 1, column=0, columnspan=2, pady=10)

    def select_columns(self, window):
        """
        Procesa las columnas seleccionadas y las combina en el DataFrame final.
        """
        try:
            # Obtener las columnas seleccionadas y sus órdenes
            selected_columns_order = sorted(
                [
                    (order.get(), index)
                    for index, order in enumerate(self.order_inputs)
                    if self.checkboxes[index].get() and order.get() > 0
                ]
            )

            if not selected_columns_order:
                messagebox.showwarning("Advertencia", "No se seleccionaron columnas o no se asignaron órdenes válidas.")
                return

            # Combinar las columnas seleccionadas en el DataFrame final
            combined_df = self.data_processor.combine_columns(self.data_processor.df, selected_columns_order)
            
            if combined_df.empty:
                messagebox.showerror("Error", "No se pudieron combinar las columnas seleccionadas.")
                return

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Columnas agregadas correctamente.")

            # Avanzar al siguiente archivo
            window.destroy()
            # Actualizar la ventana principal (sin destruirla)
            self.update_main_window()
            self.process_next_file()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar las columnas: {str(e)}")

    def update_main_window(self):
        """
        Actualiza la ventana principal sin destruirla.
        """
        for widget in self.root.winfo_children():
            widget.pack_forget()  # Oculta los elementos existentes

        # Vuelve a mostrar las opciones finales
        self.show_final_options()

    def show_final_options(self):
        """
        Muestra opciones finales después de procesar todos los archivos.
        """
        ttk.Button(
            self.root,
            text="Generar archivo combinado",
            command=self.generate_combined_file
        ).pack(pady=20)

        ttk.Button(
            self.root,
            text="Agregar columna desde archivo de referencia",
            command=self.upload_reference_file
        ).pack(pady=10)

    def generate_combined_file(self):
        """
        Genera y guarda el archivo combinado.
        """
        if not self.data_processor.df_combined.empty:
            rename_window = tk.Toplevel(self.root)
            rename_window.title("Renombrar columnas")
            rename_window.configure(bg="#e0e0e0")

            tk.Label(rename_window, text="Renombra las columnas antes de guardar:", bg="#e0e0e0").pack(pady=10)

            new_column_names = []
            for idx, col in enumerate(self.data_processor.df_combined.columns):
                frame = tk.Frame(rename_window, bg="#e0e0e0")
                frame.pack(pady=5, padx=10, fill=tk.X)

                tk.Label(frame, text=f"Columna {idx + 1}: {col}", bg="#e0e0e0").pack(side=tk.LEFT)
                new_name_var = tk.StringVar(value=col)
                tk.Entry(frame, textvariable=new_name_var, width=30).pack(side=tk.RIGHT, padx=5)
                new_column_names.append(new_name_var)

            def save_file():
                renamed_columns = [var.get() for var in new_column_names]
                self.data_processor.rename_columns(renamed_columns)

                output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("XLSX files", "*.xlsx")])
                if output_file:
                    self.data_processor.save_combined_file(output_file)
                    messagebox.showinfo("Éxito", f"Archivo combinado guardado en: {output_file}")
                    rename_window.destroy()

            ttk.Button(rename_window, text="Guardar archivo", command=save_file).pack(pady=10)
        else:
            messagebox.showerror("Error", "No hay datos para combinar.")

    def upload_reference_file(self):
        """
        Muestra un cuadro de diálogo para cargar un archivo de referencia.
        """
        reference_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if reference_file:
            self.data_processor.load_reference_file(reference_file)
            self.create_reference_window()

    def create_reference_window(self):
        """
        Crea una ventana para seleccionar columnas de referencia.
        """
        self.reference_window = tk.Toplevel(self.root)
        self.reference_window.title("Columnas de referencia")
        self.reference_window.configure(bg="#e0e0e0")

        tk.Label(self.reference_window, text="Selecciona la columna de EAN y la columna a agregar:", bg="#e0e0e0").pack(pady=10)
        self.id_column_var = tk.StringVar()
        self.column_to_add_var = tk.StringVar()

        tk.Label(self.reference_window, text="Columna de EAN:", bg="#e0e0e0").pack(pady=5)
        tk.Entry(self.reference_window, textvariable=self.id_column_var).pack(pady=5)

        tk.Label(self.reference_window, text="Columna a agregar:", bg="#e0e0e0").pack(pady=5)
        tk.Entry(self.reference_window, textvariable=self.column_to_add_var).pack(pady=5)

        ttk.Button(self.reference_window, text="Agregar columna", command=self.add_reference_column).pack(pady=10)

    def add_reference_column(self):
        """
        Lógica para agregar columnas desde el archivo de referencia.
        """
        try:
            id_column_index = int(self.id_column_var.get().strip()) - 1
            column_to_add_index = int(self.column_to_add_var.get().strip()) - 1

            updated_df, added_column = self.data_processor.add_reference_column(id_column_index, column_to_add_index)
            messagebox.showinfo("Éxito", f"La columna '{added_column}' se ha agregado correctamente.")
            self.reference_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa índices válidos para las columnas.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
