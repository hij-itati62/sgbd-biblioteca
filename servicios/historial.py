"""Historial de acciones como pila LIFO."""
from typing import Any, List, Optional


class HistorialAcciones:
    """Pila de historial usando lista Python."""

    def __init__(self):
        self._historial: List[Any] = []

    def push(self, accion: Any) -> None:
        self._historial.append(accion)

    def pop(self) -> Optional[Any]:
        if not self._historial:
            return None
        return self._historial.pop()

    def ver_todos(self) -> List[Any]:
        return self._historial.copy()