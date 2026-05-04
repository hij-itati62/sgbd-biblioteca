"""Jerarquía de usuarios: Alumno, Profesor, Administrador."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict

from modelos.entidad import Entidad
from utils.constantes import MAX_LIBROS_ALUMNO, MAX_LIBROS_PROFESOR


class Usuario(Entidad, ABC):
    """Clase abstracta base para todos los usuarios."""

    def __init__(self, nombre: str, email: str, contraseña_hash: str) -> None:
        super().__init__()
        self._nombre = nombre.strip()
        self._email = email.strip().lower()
        self._contraseña_hash = contraseña_hash
        self._prestamos_activos: list = []  # lista de ISBNs

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @property
    def contraseña_hash(self) -> str:
        return self._contraseña_hash

    @property
    def prestamos_activos(self) -> list:
        return self._prestamos_activos.copy()

    def agregar_prestamo(self, isbn: str) -> None:
        self._prestamos_activos.append(isbn)

    def eliminar_prestamo(self, isbn: str) -> None:
        if isbn in self._prestamos_activos:
            self._prestamos_activos.remove(isbn)

    @abstractmethod
    def puede_pedir_prestado(self) -> bool:
        """Determina si el usuario puede pedir más libros prestados."""
        pass

    @abstractmethod
    def calcular_multa(self, dias_retraso: int) -> float:
        """Calcula multa por retraso según tipo de usuario."""
        pass

    def __str__(self) -> str:
        return f"{self.nombre} ({self.email})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self.email == other.email

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "nombre": self.nombre,
            "email": self.email,
            "contraseña_hash": self.contraseña_hash,
            "prestamos_activos": self.prestamos_activos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        tipo = data.get("tipo")
        if tipo == "Alumno":
            from modelos.usuario import Alumno
            return Alumno.from_dict(data)
        elif tipo == "Profesor":
            from modelos.usuario import Profesor
            return Profesor.from_dict(data)
        elif tipo == "Administrador":
            from modelos.usuario import Administrador
            return Administrador.from_dict(data)
        else:
            raise ValueError(f"Tipo de usuario desconocido: {tipo}")


class Alumno(Usuario):
    def __init__(
        self,
        nombre: str,
        email: str,
        contraseña_hash: str,
        carrera: str,
        semestre: int,
    ) -> None:
        super().__init__(nombre, email, contraseña_hash)
        self.carrera = carrera
        self.semestre = semestre
        self.max_libros = MAX_LIBROS_ALUMNO

    def puede_pedir_prestado(self) -> bool:
        return len(self.prestamos_activos) < self.max_libros

    def calcular_multa(self, dias_retraso: int) -> float:
        if dias_retraso <= 0:
            return 0.0
        multa = dias_retraso * 5.0  # $5 MXN/día
        if dias_retraso > 30:
            multa *= 1.2
        return multa

    def __str__(self) -> str:
        return f"Alumno: {self.nombre} ({self.carrera}, semestre {self.semestre})"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "carrera": self.carrera,
            "semestre": self.semestre,
            "max_libros": self.max_libros,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alumno":
        usuario = cls(
            nombre=data["nombre"],
            email=data["email"],
            contraseña_hash=data["contraseña_hash"],
            carrera=data["carrera"],
            semestre=data["semestre"],
        )
        usuario._id = data["id"]
        usuario._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        usuario._prestamos_activos = data["prestamos_activos"]
        return usuario


class Profesor(Usuario):
    def __init__(
        self,
        nombre: str,
        email: str,
        contraseña_hash: str,
        departamento: str,
    ) -> None:
        super().__init__(nombre, email, contraseña_hash)
        self.departamento = departamento
        self.max_libros = MAX_LIBROS_PROFESOR

    def puede_pedir_prestado(self) -> bool:
        return len(self.prestamos_activos) < self.max_libros

    def calcular_multa(self, dias_retraso: int) -> float:
        if dias_retraso <= 0:
            return 0.0
        multa = dias_retraso * 2.0  # $2 MXN/día
        if dias_retraso > 30:
            multa *= 1.2
        return multa

    def __str__(self) -> str:
        return f"Profesor: {self.nombre} ({self.departamento})"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "departamento": self.departamento,
            "max_libros": self.max_libros,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profesor":
        usuario = cls(
            nombre=data["nombre"],
            email=data["email"],
            contraseña_hash=data["contraseña_hash"],
            departamento=data["departamento"],
        )
        usuario._id = data["id"]
        usuario._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        usuario._prestamos_activos = data["prestamos_activos"]
        return usuario


class Administrador(Usuario):
    def __init__(
        self,
        nombre: str,
        email: str,
        contraseña_hash: str,
        nivel_acceso: int,
    ) -> None:
        super().__init__(nombre, email, contraseña_hash)
        self.nivel_acceso = nivel_acceso
        self.max_libros = 0  # Los admins no piden prestado directamente

    def puede_pedir_prestado(self) -> bool:
        return False  # Los administradores no toman préstamos

    def calcular_multa(self, dias_retraso: int) -> float:
        return 0.0  # Administradores no pagan multa

    def __str__(self) -> str:
        return f"Administrador: {self.nombre} (Nivel {self.nivel_acceso})"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({"nivel_acceso": self.nivel_acceso})
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Administrador":
        usuario = cls(
            nombre=data["nombre"],
            email=data["email"],
            contraseña_hash=data["contraseña_hash"],
            nivel_acceso=data["nivel_acceso"],
        )
        usuario._id = data["id"]
        usuario._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        usuario._prestamos_activos = data["prestamos_activos"]
        return usuario