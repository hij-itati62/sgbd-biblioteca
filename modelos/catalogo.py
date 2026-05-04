"""Catálogo central del sistema con persistencia y búsqueda."""
import json
from pathlib import Path
from typing import List, Dict, Optional, Protocol, Any, Tuple
from collections import deque, Counter, defaultdict
import unicodedata

from modelos.libro import Libro, LibroDigital, LibroFisico
from modelos.usuario import Usuario, Alumno, Profesor, Administrador
from modelos.prestamo import Prestamo


class Buscable(Protocol):
    """Protocolo que define objetos que pueden buscar."""

    def buscar(self, query: str) -> List[Libro]:
        """Retorna lista de libros que coinciden con la búsqueda."""
        ...


class Catalogo:
    """
    Gestor principal de la biblioteca. Implementa Buscable.
    """

    def __init__(self) -> None:
        self.libros: List[Libro] = []
        self.usuarios: Dict[str, Usuario] = {}  # clave = email
        self.prestamos: List[Prestamo] = []
        self.cola_espera: deque = deque()  # (email_usuario, isbn_libro)

    # ---------- CRUD Libros ----------
    def agregar_libro(self, libro: Libro) -> None:
        if any(l.isbn == libro.isbn for l in self.libros):
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn}")
        self.libros.append(libro)

    def eliminar_libro(self, isbn: str) -> bool:
        for i, libro in enumerate(self.libros):
            if libro.isbn == isbn:
                self.libros.pop(i)
                return True
        return False

    # ---------- Búsqueda (Protocolo Buscable) ----------
    def buscar(self, query: str) -> List[Libro]:
        """
        Busca libros por título, autor o ISBN (case-insensitive).
        Usa comprensión de listas.
        """
        q = query.lower()
        return [libro for libro in self.libros if libro.buscar_coincidencia(q)]

    def listar_disponibles(self) -> List[Libro]:
        return [libro for libro in self.libros if libro.disponible]

    # ---------- Gestión de usuarios ----------
    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.email in self.usuarios:
            raise ValueError(f"El usuario con email {usuario.email} ya existe")
        self.usuarios[usuario.email] = usuario

    def eliminar_usuario(self, email: str) -> bool:
        if email in self.usuarios:
            del self.usuarios[email]
            return True
        return False

    # ---------- Préstamos ----------
    def registrar_prestamo(self, email_usuario: str, isbn_libro: str) -> bool:
        """Registra un préstamo si es posible."""
        usuario = self.usuarios.get(email_usuario)
        if not usuario or not usuario.puede_pedir_prestado():
            return False

        libro = next((l for l in self.libros if l.isbn == isbn_libro), None)
        if not libro or not libro.disponible:
            # Si no está disponible, encolar
            self.cola_espera.append((email_usuario, isbn_libro))
            return False

        # Realizar préstamo
        prestamo = Prestamo(email_usuario, isbn_libro)
        self.prestamos.append(prestamo)
        usuario.agregar_prestamo(isbn_libro)
        libro._disponible = False  # Acceso controlado
        return True

    def procesar_devolucion(self, isbn_libro: str, email_usuario: str) -> bool:
        """Procesa devolución y atiende siguiente en cola de espera."""
        usuario = self.usuarios.get(email_usuario)
        if not usuario:
            return False

        libro = next((l for l in self.libros if l.isbn == isbn_libro), None)
        if not libro:
            return False

        # Buscar préstamo activo
        prestamo_activo = next(
            (p for p in self.prestamos if p.isbn_libro == isbn_libro and p.email_usuario == email_usuario and p.esta_activo),
            None
        )
        if not prestamo_activo:
            return False

        prestamo_activo.cerrar()
        usuario.eliminar_prestamo(isbn_libro)
        libro.devolver()

        # Atender cola de espera
        self._atender_cola_espera(isbn_libro)
        return True

    def _atender_cola_espera(self, isbn_libro: str) -> None:
        """Atiende la cola de espera para un libro específico."""
        # Este método es interno y simplificado para el ejemplo.
        pass

    def ver_cola_espera(self) -> List[Tuple[str, str]]:
        return list(self.cola_espera)

    # ---------- Reportes ----------
    def generar_reporte(self) -> str:
        """Genera un reporte completo con estadísticas."""
        # Libros más prestados
        contador_libros = Counter(p.isbn_libro for p in self.prestamos)
        libro_mas_prestado = contador_libros.most_common(1)
        libro_mas_prestado_str = libro_mas_prestado[0][0] if libro_mas_prestado else "Ninguno"

        # Usuario con más préstamos
        contador_usuarios = Counter(p.email_usuario for p in self.prestamos)
        usuario_top = contador_usuarios.most_common(1)
        usuario_top_str = usuario_top[0][0] if usuario_top else "Ninguno"

        # Multa promedio (simplificado)
        multas = []
        for p in self.prestamos:
            if not p.esta_activo:
                usuario = self.usuarios.get(p.email_usuario)
                if usuario:
                    multas.append(usuario.calcular_multa(p.dias_retraso()))

        multa_promedio = sum(multas) / len(multas) if multas else 0.0

        # Distribución por género
        por_genero: Dict[str, int] = defaultdict(int)
        for libro in self.libros:
            por_genero[libro.genero] += 1

        reporte = f"""
=== REPORTE DE BIBLIOTECA ===
Libros totales: {len(self.libros)}
Usuarios registrados: {len(self.usuarios)}
Préstamos realizados: {len(self.prestamos)}
Préstamos activos: {sum(1 for p in self.prestamos if p.esta_activo)}
Libro más prestado: {libro_mas_prestado_str}
Usuario con más préstamos: {usuario_top_str}
Multa promedio: ${multa_promedio:.2f} MXN
Distribución por género: {dict(por_genero)}
"""
        return reporte

    # ---------- Persistencia JSON ----------
    def guardar_json(self, ruta: Path) -> None:
        """Guarda todo el estado del catálogo en JSON."""
        datos = {
            "libros": [libro.to_dict() for libro in self.libros],
            "usuarios": [usuario.to_dict() for usuario in self.usuarios.values()],
            "prestamos": [prestamo.to_dict() for prestamo in self.prestamos],
            "cola_espera": list(self.cola_espera),
        }
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def cargar_json(self, ruta: Path) -> None:
        """Carga el estado del catálogo desde JSON."""
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Limpiar estado actual
        self.libros.clear()
        self.usuarios.clear()
        self.prestamos.clear()
        self.cola_espera.clear()

        # Cargar libros
        from modelos.libro import Libro
        for libro_dict in datos.get("libros", []):
            libro = Libro.from_dict(libro_dict)
            self.libros.append(libro)

        # Cargar usuarios
        from modelos.usuario import Usuario
        for usuario_dict in datos.get("usuarios", []):
            usuario = Usuario.from_dict(usuario_dict)
            self.usuarios[usuario.email] = usuario

        # Cargar préstamos
        for prestamo_dict in datos.get("prestamos", []):
            prestamo = Prestamo.from_dict(prestamo_dict)
            self.prestamos.append(prestamo)

        # Cargar cola de espera
        self.cola_espera.extend(datos.get("cola_espera", []))