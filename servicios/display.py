"""Funciones polimórficas de visualización."""
from typing import List, Any
from modelos.entidad import Entidad


def mostrar_info(item: Entidad) -> None:
    """
    Muestra información de cualquier entidad polimórficamente.

    Args:
        item: Cualquier objeto que herede de Entidad.
    """
    print(str(item))


def generar_reporte(items: List[Any]) -> str:
    """
    Duck typing: asume que cada item tiene to_dict().
    """
    if not items:
        return "No hay elementos para reportar."

    lineas = []
    for item in items:
        try:
            data = item.to_dict()
            # Intento básico de mostrar algo legible
            lineas.append(str(item))
        except AttributeError:
            lineas.append(str(item))
    return "\n".join(lineas)