from pathlib import Path

from modelos.catalogo import Catalogo
from modelos.libro import LibroFisico, LibroDigital
from modelos.usuario import Alumno, Profesor, Administrador


RUTA_DATOS = Path("datos/biblioteca.json")


def agregar_libro(catalogo):
    tipo = input("Tipo de libro (fisico/digital): ").lower()
    titulo = input("Título: ")
    autor = input("Autor: ")
    isbn = input("ISBN-13: ")
    anio = int(input("Año: "))
    genero = input("Género: ")

    if tipo == "digital":
        formato = input("Formato (PDF/EPUB/MOBI): ")
        tamaño_mb = float(input("Tamaño MB: "))
        url = input("URL descarga: ")

        libro = LibroDigital(titulo, autor, isbn, anio, genero, formato, tamaño_mb, url)

    else:
        ubicacion = input("Ubicación: ")
        ejemplares = int(input("Número de ejemplares: "))

        libro = LibroFisico(titulo, autor, isbn, anio, genero, ubicacion, ejemplares)

    catalogo.agregar_libro(libro)
    print("Libro agregado correctamente.")


def buscar_libro(catalogo):
    query = input("Buscar por título, autor o ISBN: ")
    resultados = catalogo.buscar(query)

    if not resultados:
        print("No se encontraron libros.")
        return

    for libro in resultados:
        print(libro)


def registrar_usuario(catalogo):
    tipo = input("Tipo de usuario (alumno/profesor/admin): ").lower()
    nombre = input("Nombre: ")
    email = input("Email: ")
    contraseña = input("Contraseña: ")

    if tipo == "alumno":
        carrera = input("Carrera: ")
        semestre = int(input("Semestre: "))
        usuario = Alumno(nombre, email, contraseña, carrera, semestre)

    elif tipo == "profesor":
        departamento = input("Departamento: ")
        usuario = Profesor(nombre, email, contraseña, departamento)

    else:
        nivel = int(input("Nivel de acceso: "))
        usuario = Administrador(nombre, email, contraseña, nivel)

    catalogo.registrar_usuario(usuario)
    print("Usuario registrado correctamente.")


def prestar_libro(catalogo):
    email = input("Email del usuario: ")
    isbn = input("ISBN del libro: ")

    ok = catalogo.registrar_prestamo(email, isbn)

    if ok:
        print("Préstamo registrado correctamente.")
    else:
        print("No se pudo prestar. Usuario inválido, límite alcanzado o libro no disponible.")


def devolver_libro(catalogo):
    email = input("Email del usuario: ")
    isbn = input("ISBN del libro: ")

    ok = catalogo.procesar_devolucion(isbn, email)

    if ok:
        print("Libro devuelto correctamente.")
    else:
        print("No se pudo devolver el libro.")


def ver_cola(catalogo):
    cola = catalogo.ver_cola_espera()

    if not cola:
        print("La cola está vacía.")
        return

    for email, isbn in cola:
        print(f"Usuario: {email} | ISBN: {isbn}")


def guardar(catalogo):
    RUTA_DATOS.parent.mkdir(exist_ok=True)
    catalogo.guardar_json(RUTA_DATOS)
    print("Datos guardados correctamente.")


def main():
    catalogo = Catalogo()

    try:
        catalogo.cargar_json(RUTA_DATOS)
        print("Datos cargados correctamente.")
    except FileNotFoundError:
        print("No hay datos previos.")
    except Exception as e:
        print("No se pudieron cargar los datos:", e)

    while True:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1. Agregar libro")
        print("2. Buscar libro")
        print("3. Registrar usuario")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Ver cola de espera")
        print("7. Reportes")
        print("8. Guardar")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        try:
            match opcion:
                case "1":
                    agregar_libro(catalogo)

                case "2":
                    buscar_libro(catalogo)

                case "3":
                    registrar_usuario(catalogo)

                case "4":
                    prestar_libro(catalogo)

                case "5":
                    devolver_libro(catalogo)

                case "6":
                    ver_cola(catalogo)

                case "7":
                    print(catalogo.generar_reporte())

                case "8":
                    guardar(catalogo)

                case "0":
                    guardar(catalogo)
                    print("Saliendo del sistema.")
                    break

                case _:
                    print("Opción inválida.")

        except ValueError as e:
            print("Error de valor:", e)

        except KeyError as e:
            print("Error de clave:", e)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()