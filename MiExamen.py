from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.catalogo import Catalogo
from modelos.libro import LibroFisico, LibroDigital
from modelos.usuario import Alumno, Profesor, Administrador


RUTA_DATOS = Path("datos/biblioteca.json")


class MiExamenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca Digital")
        self.root.geometry("900x600")

        self.catalogo = Catalogo()
        self.cargar_datos()

        titulo = tk.Label(
            root,
            text="📚 Sistema de Gestión de Biblioteca Digital",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        botones = [
            ("Agregar libro", self.ventana_agregar_libro),
            ("Buscar libro", self.ventana_buscar_libro),
            ("Registrar usuario", self.ventana_registrar_usuario),
            ("Prestar libro", self.ventana_prestar_libro),
            ("Devolver libro", self.ventana_devolver_libro),
            ("Ver cola", self.ver_cola),
            ("Reportes", self.ver_reporte),
            ("Guardar", self.guardar_datos),
        ]

        for texto, comando in botones:
            tk.Button(
                frame_botones,
                text=texto,
                width=18,
                command=comando
            ).pack(side=tk.LEFT, padx=5, pady=5)

        self.salida = tk.Text(root, height=22, width=105)
        self.salida.pack(pady=10)

        self.mostrar("Sistema iniciado correctamente.")

    def mostrar(self, texto):
        self.salida.delete("1.0", tk.END)
        self.salida.insert(tk.END, texto)

    def cargar_datos(self):
        try:
            self.catalogo.cargar_json(RUTA_DATOS)
        except FileNotFoundError:
            RUTA_DATOS.parent.mkdir(exist_ok=True)
        except Exception as e:
            messagebox.showwarning("Aviso", f"No se pudieron cargar datos: {e}")

    def guardar_datos(self):
        try:
            RUTA_DATOS.parent.mkdir(exist_ok=True)
            self.catalogo.guardar_json(RUTA_DATOS)
            messagebox.showinfo("Guardado", "Datos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ventana_agregar_libro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar libro")
        ventana.geometry("400x450")

        campos = {}

        etiquetas = [
            "Título", "Autor", "ISBN", "Año", "Género",
            "Tipo", "Formato/Ubicación", "Tamaño MB/Ejemplares", "URL"
        ]

        for etiqueta in etiquetas:
            tk.Label(ventana, text=etiqueta).pack()
            entrada = tk.Entry(ventana, width=40)
            entrada.pack()
            campos[etiqueta] = entrada

        campos["Tipo"].insert(0, "fisico")
        campos["Formato/Ubicación"].insert(0, "Estante A-1")
        campos["Tamaño MB/Ejemplares"].insert(0, "1")
        campos["URL"].insert(0, "https://ejemplo.com/libro.pdf")

        def guardar():
            try:
                tipo = campos["Tipo"].get().lower()

                if tipo == "digital":
                    libro = LibroDigital(
                        titulo=campos["Título"].get(),
                        autor=campos["Autor"].get(),
                        isbn=campos["ISBN"].get(),
                        anio=int(campos["Año"].get()),
                        genero=campos["Género"].get(),
                        formato=campos["Formato/Ubicación"].get(),
                        tamaño_mb=float(campos["Tamaño MB/Ejemplares"].get()),
                        url_descarga=campos["URL"].get()
                    )
                else:
                    libro = LibroFisico(
                        titulo=campos["Título"].get(),
                        autor=campos["Autor"].get(),
                        isbn=campos["ISBN"].get(),
                        anio=int(campos["Año"].get()),
                        genero=campos["Género"].get(),
                        ubicacion=campos["Formato/Ubicación"].get(),
                        num_ejemplares=int(campos["Tamaño MB/Ejemplares"].get())
                    )

                self.catalogo.agregar_libro(libro)
                self.guardar_datos()
                self.mostrar(f"Libro agregado:\n{libro}")
                ventana.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar libro", command=guardar).pack(pady=15)

    def ventana_buscar_libro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar libro")
        ventana.geometry("350x150")

        tk.Label(ventana, text="Buscar por título, autor o ISBN").pack()
        entrada = tk.Entry(ventana, width=40)
        entrada.pack(pady=10)

        def buscar():
            resultados = self.catalogo.buscar(entrada.get())

            if resultados:
                texto = "\n\n".join(str(libro) for libro in resultados)
            else:
                texto = "No se encontraron libros."

            self.mostrar(texto)
            ventana.destroy()

        tk.Button(ventana, text="Buscar", command=buscar).pack()

    def ventana_registrar_usuario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar usuario")
        ventana.geometry("400x400")

        campos = {}

        etiquetas = [
            "Nombre", "Email", "Contraseña", "Tipo",
            "Carrera/Departamento/Nivel", "Semestre"
        ]

        for etiqueta in etiquetas:
            tk.Label(ventana, text=etiqueta).pack()
            entrada = tk.Entry(ventana, width=40)
            entrada.pack()
            campos[etiqueta] = entrada

        campos["Tipo"].insert(0, "alumno")
        campos["Semestre"].insert(0, "1")

        def guardar():
            try:
                tipo = campos["Tipo"].get().lower()

                if tipo == "alumno":
                    usuario = Alumno(
                        nombre=campos["Nombre"].get(),
                        email=campos["Email"].get(),
                        contraseña_hash=campos["Contraseña"].get(),
                        carrera=campos["Carrera/Departamento/Nivel"].get(),
                        semestre=int(campos["Semestre"].get())
                    )
                elif tipo == "profesor":
                    usuario = Profesor(
                        nombre=campos["Nombre"].get(),
                        email=campos["Email"].get(),
                        contraseña_hash=campos["Contraseña"].get(),
                        departamento=campos["Carrera/Departamento/Nivel"].get()
                    )
                else:
                    usuario = Administrador(
                        nombre=campos["Nombre"].get(),
                        email=campos["Email"].get(),
                        contraseña_hash=campos["Contraseña"].get(),
                        nivel_acceso=int(campos["Carrera/Departamento/Nivel"].get())
                    )

                self.catalogo.registrar_usuario(usuario)
                self.guardar_datos()
                self.mostrar(f"Usuario registrado:\n{usuario}")
                ventana.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar usuario", command=guardar).pack(pady=15)

    def ventana_prestar_libro(self):
        self.ventana_email_isbn("Prestar libro", self.prestar_libro)

    def ventana_devolver_libro(self):
        self.ventana_email_isbn("Devolver libro", self.devolver_libro)

    def ventana_email_isbn(self, titulo, accion):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("350x200")

        tk.Label(ventana, text="Email usuario").pack()
        email = tk.Entry(ventana, width=40)
        email.pack()

        tk.Label(ventana, text="ISBN libro").pack()
        isbn = tk.Entry(ventana, width=40)
        isbn.pack()

        def ejecutar():
            accion(email.get(), isbn.get())
            ventana.destroy()

        tk.Button(ventana, text=titulo, command=ejecutar).pack(pady=15)

    def prestar_libro(self, email, isbn):
        try:
            ok = self.catalogo.registrar_prestamo(email, isbn)
            self.guardar_datos()

            if ok:
                self.mostrar("Préstamo registrado correctamente.")
            else:
                self.mostrar("No se pudo prestar. Puede estar no disponible o usuario inválido.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def devolver_libro(self, email, isbn):
        try:
            ok = self.catalogo.procesar_devolucion(isbn, email)
            self.guardar_datos()

            if ok:
                self.mostrar("Libro devuelto correctamente.")
            else:
                self.mostrar("No se pudo devolver el libro.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_cola(self):
        cola = self.catalogo.ver_cola_espera()

        if cola:
            texto = "\n".join(f"Usuario: {email} | ISBN: {isbn}" for email, isbn in cola)
        else:
            texto = "La cola está vacía."

        self.mostrar(texto)

    def ver_reporte(self):
        self.mostrar(self.catalogo.generar_reporte())


if __name__ == "__main__":
    root = tk.Tk()
    app = MiExamenApp(root)
    root.mainloop()