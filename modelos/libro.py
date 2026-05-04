"""Clases relacionadas con libros: Libro base, Digital y Físico."""
import unicodedata
from datetime import datetime
from typing import Any, Dict
from abc import ABC

from modelos.entidad import Entidad
from utils.validadores import validar_isbn13
from utils.constantes import ANIO_MINIMO


class Libro(Entidad, ABC):
    """Clase abstracta base para todo tipo de libro."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        disponible: bool = True,
    ) -> None:
        super().__init__()
        self._titulo = titulo.strip()
        self._autor = autor.strip()
        self.isbn = isbn
        self.anio = anio
        self._genero = genero.strip()
        self._disponible = disponible

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        if not validar_isbn13(valor):
            raise ValueError(f"ISBN inválido: {valor}")
        self._isbn = valor

    @property
    def anio(self) -> int:
        return self._anio

    @anio.setter
    def anio(self, valor: int) -> None:
        anio_actual = datetime.now().year
        if not (ANIO_MINIMO <= valor <= anio_actual):
            raise ValueError(f"Año {valor} fuera de rango ({ANIO_MINIMO}-{anio_actual})")
        self._anio = valor

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def disponible(self) -> bool:
        return self._disponible

    def devolver(self) -> None:
        """Marca el libro como disponible."""
        self._disponible = True

    def buscar_coincidencia(self, query: str) -> bool:
        """
        Verifica si el libro coincide con la búsqueda (título, autor o ISBN).
        Búsqueda case-insensitive.
        """
        q = query.lower()
        return (q in self.titulo.lower()) or (q in self.autor.lower()) or (q in self.isbn)

    def __str__(self) -> str:
        return f"{self.titulo} ({self.anio}) - {self.autor} | ISBN: {self.isbn} | {'Disponible' if self.disponible else 'Prestado'}"

    def __repr__(self) -> str:
        return f"<Libro(isbn={self.isbn}, titulo={self.titulo})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Libro):
            return False
        return self.isbn == other.isbn

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "anio": self.anio,
            "genero": self.genero,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Libro":
        """Reconstruye un libro desde diccionario."""
        # Determinar tipo específico
        tipo = data.get("tipo")
        if tipo == "LibroFisico":
            from modelos.libro import LibroFisico
            return LibroFisico.from_dict(data)
        elif tipo == "LibroDigital":
            from modelos.libro import LibroDigital
            return LibroDigital.from_dict(data)
        else:
            # Genérico
            libro = cls.__new__(cls)
            libro._id = data["id"]
            libro._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
            libro._titulo = data["titulo"]
            libro._autor = data["autor"]
            libro._isbn = data["isbn"]
            libro._anio = data["anio"]
            libro._genero = data["genero"]
            libro._disponible = data["disponible"]
            return libro


class LibroDigital(Libro):
    """Libro en formato digital con URL de descarga."""

    FORMATOS_VALIDOS = {"PDF", "EPUB", "MOBI"}

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        formato: str,
        tamaño_mb: float,
        url_descarga: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(titulo, autor, isbn, anio, genero, disponible)
        self.formato = formato
        self.tamaño_mb = tamaño_mb
        self.url_descarga = url_descarga

    @property
    def formato(self) -> str:
        return self._formato

    @formato.setter
    def formato(self, valor: str) -> None:
        if valor.upper() not in self.FORMATOS_VALIDOS:
            raise ValueError(f"Formato inválido: {valor}. Permitidos: {self.FORMATOS_VALIDOS}")
        self._formato = valor.upper()

    @property
    def tamaño_mb(self) -> float:
        return self._tamaño_mb

    @tamaño_mb.setter
    def tamaño_mb(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El tamaño debe ser positivo")
        self._tamaño_mb = valor

    @property
    def url_descarga(self) -> str:
        return self._url_descarga

    @url_descarga.setter
    def url_descarga(self, valor: str) -> None:
        if not valor.startswith(("http://", "https://")):
            raise ValueError("URL debe comenzar con http:// o https://")
        self._url_descarga = valor

    def descargar(self) -> str:
        return f"Descargando {self.titulo} desde {self.url_descarga}"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} [Digital: {self.formato}, {self.tamaño_mb} MB]"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "formato": self.formato,
            "tamaño_mb": self.tamaño_mb,
            "url_descarga": self.url_descarga,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LibroDigital":
        libro = cls(
            titulo=data["titulo"],
            autor=data["autor"],
            isbn=data["isbn"],
            anio=data["anio"],
            genero=data["genero"],
            formato=data["formato"],
            tamaño_mb=data["tamaño_mb"],
            url_descarga=data["url_descarga"],
            disponible=data["disponible"],
        )
        libro._id = data["id"]
        libro._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        return libro


class LibroFisico(Libro):
    """Libro físico con ubicación y número de ejemplares."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        ubicacion: str,
        num_ejemplares: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(titulo, autor, isbn, anio, genero, disponible)
        self.ubicacion = ubicacion
        self.num_ejemplares = num_ejemplares

    @property
    def ubicacion(self) -> str:
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("La ubicación no puede estar vacía")
        self._ubicacion = valor.strip()

    @property
    def num_ejemplares(self) -> int:
        return self._num_ejemplares

    @num_ejemplares.setter
    def num_ejemplares(self, valor: int) -> None:
        if valor < 1:
            raise ValueError("Debe haber al menos un ejemplar")
        self._num_ejemplares = valor

    def reservar(self) -> str:
        return f"Reservado ejemplar de {self.titulo} en {self.ubicacion}"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} [Físico: {self.ubicacion}, {self.num_ejemplares} ejemplares]"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "ubicacion": self.ubicacion,
            "num_ejemplares": self.num_ejemplares,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LibroFisico":
        libro = cls(
            titulo=data["titulo"],
            autor=data["autor"],
            isbn=data["isbn"],
            anio=data["anio"],
            genero=data["genero"],
            ubicacion=data["ubicacion"],
            num_ejemplares=data["num_ejemplares"],
            disponible=data["disponible"],
        )
        libro._id = data["id"]
        libro._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        return libro