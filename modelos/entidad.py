"""Clase base abstracta Entidad para todo el sistema."""
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from typing import Any, Dict


class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    Proporciona ID único y fecha de creación automáticos.
    """

    def __init__(self) -> None:
        """Inicializa una entidad con ID único y timestamp de creación."""
        self._id: str = str(uuid.uuid4())
        self._fecha_creacion: datetime = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha de creación."""
        return self._fecha_creacion

    @abstractmethod
    def __str__(self) -> str:
        """Representación en string de la entidad."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario para JSON."""
        pass