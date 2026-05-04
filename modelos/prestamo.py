"""Clase Préstamo que gestiona préstamos de libros."""
from datetime import datetime, date
from typing import Optional, Dict, Any

from modelos.entidad import Entidad


class Prestamo(Entidad):
    """Representa un préstamo de un libro a un usuario."""

    def __init__(
        self,
        email_usuario: str,
        isbn_libro: str,
        fecha_prestamo: Optional[datetime] = None,
        fecha_devolucion_esperada: Optional[date] = None,
    ) -> None:
        super().__init__()
        self.email_usuario = email_usuario
        self.isbn_libro = isbn_libro
        self.fecha_prestamo = fecha_prestamo or datetime.now()
        self.fecha_devolucion_esperada = fecha_devolucion_esperada or (
            self.fecha_prestamo.date() + date.today().replace(year=date.today().year + 1).replace(day=1)  # simplificado: 30 días
        )
        self.fecha_devolucion_real: Optional[datetime] = None

    def cerrar(self, fecha_devolucion: Optional[datetime] = None) -> None:
        """Cierra el préstamo al devolver el libro."""
        self.fecha_devolucion_real = fecha_devolucion or datetime.now()

    @property
    def esta_activo(self) -> bool:
        return self.fecha_devolucion_real is None

    def dias_retraso(self, fecha_referencia: Optional[datetime] = None) -> int:
        """Calcula días de retraso (negativo si no hay retraso)."""
        if not self.esta_activo:
            fecha_dev = self.fecha_devolucion_real
        else:
            fecha_dev = fecha_referencia or datetime.now()

        esperada = self.fecha_devolucion_esperada
        devolucion = fecha_dev.date() if isinstance(fecha_dev, datetime) else fecha_dev

        delta = (devolucion - esperada).days
        return max(0, delta)

    def __str__(self) -> str:
        estado = "Activo" if self.esta_activo else "Devuelto"
        return f"Préstamo: {self.email_usuario} → ISBN {self.isbn_libro} [{estado}]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "email_usuario": self.email_usuario,
            "isbn_libro": self.isbn_libro,
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion_esperada": self.fecha_devolucion_esperada.isoformat(),
            "fecha_devolucion_real": self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prestamo":
        prestamo = cls(
            email_usuario=data["email_usuario"],
            isbn_libro=data["isbn_libro"],
            fecha_prestamo=datetime.fromisoformat(data["fecha_prestamo"]),
        )
        prestamo._id = data["id"]
        prestamo._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        prestamo.fecha_devolucion_esperada = data["fecha_devolucion_esperada"]
        prestamo.fecha_devolucion_real = datetime.fromisoformat(data["fecha_devolucion_real"]) if data["fecha_devolucion_real"] else None
        return prestamo