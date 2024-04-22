import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Base")

        # Definir dimensiones de la ventana
        window_width = 500
        window_height = 300

        # Obtener las dimensiones de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la geometría de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Botones para elegir entre ingresar estudiante, materia, y nota, ver tabla, y editar/borrar
        tk.Button(root, text="Registrar Estudiante", command=self.ingresar_estudiante).pack(pady=10)
        tk.Button(root, text="Registrar Materia", command=self.ingresar_materia).pack(pady=10)
        tk.Button(root, text="Registrar Nota", command=self.ingresar_nota).pack(pady=10)
        tk.Button(root, text="Ver Tabla", command=self.ver_tabla).pack(pady=10)
        tk.Button(root, text="Editar/Borrar", command=self.editar_borrar).pack(pady=10)

        # Conexión a la base de datos
        try:
            self.conn = psycopg2.connect(
                dbname="NUR",
                user="postgres",
                password="1010",
                host="localhost",
                port="5432"
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)

    def ingresar_estudiante(self):
        # Ventana para ingresar nuevo estudiante
        self.ventana_ingresar = tk.Toplevel(self.root)
        self.ventana_ingresar.title("Registrar nuevo Estudiante")

        # Centrar la ventana en la pantalla
        window_width = 400
        window_height = 200
        x = (self.root.winfo_screenwidth() - window_width) // 2
        y = (self.root.winfo_screenheight() - window_height) // 2
        self.ventana_ingresar.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Crear campos de entrada para los datos del estudiante
        tk.Label(self.ventana_ingresar, text="Nombre Completo:").pack()
        self.nombre_var = tk.StringVar()
        tk.Entry(self.ventana_ingresar, textvariable=self.nombre_var).pack()

        tk.Label(self.ventana_ingresar, text="Fecha de Nacimiento (YYYY-MM-DD):").pack()
        self.fecha_nacimiento_var = tk.StringVar()
        tk.Entry(self.ventana_ingresar, textvariable=self.fecha_nacimiento_var).pack()

        tk.Label(self.ventana_ingresar, text="ID Estudiante:").pack()
        self.id_estudiante_var = tk.StringVar()
        tk.Entry(self.ventana_ingresar, textvariable=self.id_estudiante_var).pack()

        tk.Label(self.ventana_ingresar, text="Carrera:").pack()
        self.carrera_var = tk.StringVar()
        tk.Entry(self.ventana_ingresar, textvariable=self.carrera_var).pack()

        tk.Button(self.ventana_ingresar, text="Guardar", command=self.guardar_estudiante).pack()

    def ingresar_materia(self):
        # Ventana para ingresar nueva materia
        self.ventana_materia = tk.Toplevel(self.root)
        self.ventana_materia.title("Registrar Materia")

        # Centrar la ventana en la pantalla
        window_width = 400
        window_height = 200
        x = (self.root.winfo_screenwidth() - window_width) // 2
        y = (self.root.winfo_screenheight() - window_height) // 2
        self.ventana_materia.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Crear campos de entrada para los datos de la materia
        tk.Label(self.ventana_materia, text="ID Materia:").pack()
        self.id_materia_var = tk.StringVar()
        tk.Entry(self.ventana_materia, textvariable=self.id_materia_var).pack()

        tk.Label(self.ventana_materia, text="Nombre de la Materia:").pack()
        self.nombre_materia_var = tk.StringVar()
        tk.Entry(self.ventana_materia, textvariable=self.nombre_materia_var).pack()

        tk.Label(self.ventana_materia, text="Número de Créditos:").pack()
        self.creditos_var = tk.IntVar()
        tk.Entry(self.ventana_materia, textvariable=self.creditos_var).pack()

        tk.Button(self.ventana_materia, text="Guardar", command=self.guardar_materia).pack()

    def ingresar_nota(self):
        self.ventana_nota = tk.Toplevel(self.root)
        self.ventana_nota.title("Registrar Nota")

        window_width = 400
        window_height = 200
        x = (self.root.winfo_screenwidth() - window_width) // 2
        y = (self.root.winfo_screenheight() - window_height) // 2
        self.ventana_nota.geometry(f"{window_width}x{window_height}+{x}+{y}")

        tk.Label(self.ventana_nota, text="ID Nota:").pack()
        self.id_nota_var = tk.StringVar()
        tk.Entry(self.ventana_nota, textvariable=self.id_nota_var).pack()

        tk.Label(self.ventana_nota, text="ID del Estudiante:").pack()
        self.id_estudiante_nota_var = tk.StringVar()
        tk.Entry(self.ventana_nota, textvariable=self.id_estudiante_nota_var).pack()

        tk.Label(self.ventana_nota, text="ID de la Materia:").pack()
        self.id_materia_nota_var = tk.StringVar()
        tk.Entry(self.ventana_nota, textvariable=self.id_materia_nota_var).pack()

        tk.Label(self.ventana_nota, text="Registrar Nota:").pack()
        self.nota_var = tk.DoubleVar()
        tk.Entry(self.ventana_nota, textvariable=self.nota_var).pack()

        tk.Button(self.ventana_nota, text="Guardar", command=self.guardar_nota).pack()

    def editar_borrar(self):
        selected_item = self.tabla.focus()
        if selected_item:
            id_estudiante = self.tabla.item(selected_item, 'text')
            option = messagebox.askquestion("Editar/Borrar", "¿Deseas editar o borrar este estudiante?")
            if option == 'yes':
                self.editar_estudiante(id_estudiante)
            else:
                self.borrar_estudiante(id_estudiante)
        else:
            messagebox.showwarning("Editar/Borrar", "Por favor, selecciona un estudiante de la tabla.")

    def editar_estudiante(self, id_estudiante):
        pass  # Aquí implementarías la lógica para editar el estudiante seleccionado

    def borrar_estudiante(self, id_estudiante):
        pass  # Aquí implementarías la lógica para borrar el estudiante seleccionado

    def guardar_estudiante(self):
        nombre = self.nombre_var.get()
        fecha_nacimiento = self.fecha_nacimiento_var.get()
        id_estudiante = self.id_estudiante_var.get()
        carrera = self.carrera_var.get()

        try:
            self.cur.execute("SELECT id_estudiante FROM Estudiantes WHERE id_estudiante = %s", (id_estudiante,))
            resultado = self.cur.fetchone()
            if resultado:
                messagebox.showerror("Error", "El ID del estudiante ya está en uso.")
                return
        except psycopg2.Error as e:
            print("Error al verificar el ID del estudiante:", e)
            return

        try:
            self.cur.execute("INSERT INTO Estudiantes (nombre_completo, fecha_nacimiento, id_estudiante, carrera) VALUES (%s, %s, %s, %s)", (nombre, fecha_nacimiento, id_estudiante, carrera))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Estudiante ingresado correctamente.")
            self.ventana_ingresar.destroy()
            self.mostrar_datos_tabla()
        except psycopg2.Error as e:
            print("Error al ingresar estudiante:", e)
            return

    def guardar_materia(self):
        id_materia = self.id_materia_var.get()
        nombre_materia = self.nombre_materia_var.get()
        creditos = self.creditos_var.get()

        try:
            self.cur.execute("SELECT id_materia FROM Materias WHERE id_materia = %s", (id_materia,))
            resultado = self.cur.fetchone()
            if resultado:
                messagebox.showerror("Error", "El ID de la materia ya está en uso.")
                return
        except psycopg2.Error as e:
            print("Error al verificar el ID de la materia:", e)
            return

        try:
            self.cur.execute("INSERT INTO Materias (id_materia, nombre_materia, numero_creditos) VALUES (%s, %s, %s)", (id_materia, nombre_materia, creditos))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Materia agregada correctamente.")
            self.ventana_materia.destroy()
            self.mostrar_datos_tabla()
        except psycopg2.Error as e:
            print("Error al agregar materia:", e)
            return

    def guardar_nota(self):
        id_nota = self.id_nota_var.get()
        id_estudiante = self.id_estudiante_nota_var.get()
        id_materia = self.id_materia_nota_var.get()
        nota = self.nota_var.get()

        try:
            self.cur.execute("INSERT INTO Notas (id_nota, id_estudiante, id_materia, nota) VALUES (%s, %s, %s, %s)", (id_nota, id_estudiante, id_materia, nota))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Nota agregada correctamente.")
            self.ventana_nota.destroy()
            self.mostrar_datos_tabla()
        except psycopg2.Error as e:
            print("Error al agregar nota:", e)
            return

    def ver_tabla(self):
        self.ventana_tabla = tk.Toplevel(self.root)
        self.ventana_tabla.title("Tabla de Estudiantes")

        window_width = 600
        window_height = 400
        x = (self.root.winfo_screenwidth() - window_width) // 2
        y = (self.root.winfo_screenheight() - window_height) // 2
        self.ventana_tabla.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Crear tabla
        self.tabla = ttk.Treeview(self.ventana_tabla, columns=("ID", "Nombre", "Carrera", "Materia", "Nota"))
        self.tabla.heading("#0", text="ID Estudiante")
        self.tabla.column("#0", width=100)
        self.tabla.heading("#1", text="Nombre Completo")
        self.tabla.column("#1", width=150)
        self.tabla.heading("#2", text="Carrera")
        self.tabla.column("#2", width=180)
        self.tabla.heading("#3", text="Materia")
        self.tabla.column("#3", width=180)
        self.tabla.heading("#4", text="Nota")
        self.tabla.column("#4", width=100)
        self.tabla.pack(padx=30, pady=30)

        self.mostrar_datos_tabla()

    def mostrar_datos_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        try:
            self.cur.execute("""
                SELECT e.id_estudiante, e.nombre_completo, e.carrera, m.nombre_materia, n.nota
                FROM Estudiantes e
                JOIN Notas n ON e.id_estudiante = n.id_estudiante
                JOIN Materias m ON n.id_materia = m.id_materia
                ORDER BY e.id_estudiante
            """)
            estudiantes = self.cur.fetchall()
            for estudiante in estudiantes:
                self.tabla.insert("", "end", text=estudiante[0], values=(estudiante[1], estudiante[2], estudiante[3], estudiante[4]))
        except psycopg2.Error as e:
            print("Error al obtener datos de la tabla:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
