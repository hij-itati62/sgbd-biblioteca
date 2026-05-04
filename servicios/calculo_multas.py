"""Cálculo de multas con if/elif/else y match/case."""

from utils.constantes import MULTA_DIARIA_MXN, MULTA_DIARIA_PROFESOR_MXN


def calcular_multa_if(dias_retraso: int, tipo_usuario: str) -> float:
    """
    Calcula multa usando if/elif/else.

    Args:
        dias_retraso: Días de retraso (≥ 0).
        tipo_usuario: 'alumno', 'profesor' o 'admin'.

    Returns:
        Monto de la multa en MXN.
    """
    if dias_retraso <= 0:
        return 0.0

    if tipo_usuario == "alumno":
        multa_base = dias_retraso * MULTA_DIARIA_MXN
    elif tipo_usuario == "profesor":
        multa_base = dias_retraso * MULTA_DIARIA_PROFESOR_MXN
    elif tipo_usuario == "admin":
        return 0.0
    else:
        raise ValueError("Tipo de usuario no válido")

    if dias_retraso > 30:
        multa_base *= 1.2

    return round(multa_base, 2)


def calcular_multa_match(dias_retraso: int, tipo_usuario: str) -> float:
    """
    Calcula multa usando match/case (Python 3.10+).
    """
    if dias_retraso <= 0:
        return 0.0

    match tipo_usuario:
        case "alumno":
            multa_base = dias_retraso * MULTA_DIARIA_MXN
        case "profesor":
            multa_base = dias_retraso * MULTA_DIARIA_PROFESOR_MXN
        case "admin":
            return 0.0
        case _:
            raise ValueError("Tipo de usuario no válido")

    if dias_retraso > 30:
        multa_base *= 1.2

    return round(multa_base, 2)


# Demostración con prueba
if __name__ == "__main__":
    casos = [
        (0, "alumno"),
        (10, "alumno"),
        (35, "alumno"),
        (10, "profesor"),
        (35, "profesor"),
        (10, "admin"),
    ]
    for dias, tipo in casos:
        print(f"Multa (if) por {dias} días como {tipo}: ${calcular_multa_if(dias, tipo)}")
        print(f"Multa (match) por {dias} días como {tipo}: ${calcular_multa_match(dias, tipo)}")