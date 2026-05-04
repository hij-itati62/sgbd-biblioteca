"""Cola de espera FIFO con collections.deque."""
from collections import deque
from typing import Tuple, Optional, List


class GestorColaEspera:
    """Gestor de cola de espera para libros no disponibles."""

    def __init__(self):
        self._cola: deque = deque()

    def encolar_solicitud(self, usuario_email: str, isbn_libro: str) -> None:
        self._cola.append((usuario_email, isbn_libro))

    def atender_siguiente(self) -> Optional[Tuple[str, str]]:
        if not self._cola:
            return None
        return self._cola.popleft()

    def ver_cola(self) -> List[Tuple[str, str]]:
        return list(self._cola)

    def __len__(self) -> int:
        return len(self._cola)