"""Estadísticas con Counter y defaultdict."""
from collections import Counter, defaultdict
from typing import List, Dict

from modelos.prestamo import Prestamo
from modelos.libro import Libro


def libro_mas_prestado(prestamos: List[Prestamo]) -> str:
    contador = Counter(p.isbn_libro for p in prestamos)
    if not contador:
        return "Ninguno"
    return contador.most_common(1)[0][0]


def usuario_con_mas_prestamos(prestamos: List[Prestamo]) -> str:
    contador = Counter(p.email_usuario for p in prestamos)
    if not contador:
        return "Ninguno"
    return contador.most_common(1)[0][0]


def multa_promedio(prestamos: List[Prestamo], usuarios) -> float:
    """Requiere acceso a usuarios para calcular multa."""
    multas = []
    for p in prestamos:
        if not p.esta_activo:
            usuario = usuarios.get(p.email_usuario)
            if usuario:
                multas.append(usuario.calcular_multa(p.dias_retraso()))
    if not multas:
        return 0.0
    return sum(multas) / len(multas)


def distribucion_por_genero(libros: List[Libro]) -> Dict[str, int]:
    distribucion = defaultdict(int)
    for libro in libros:
        distribucion[libro.genero] += 1
    return dict(distribucion)