"""Funciones de validación: ISBN-13 y email."""

def validar_isbn13(isbn: str) -> bool:
    """
    Valida un ISBN-13 según algoritmo estándar.

    Args:
        isbn: String de 13 dígitos.

    Returns:
        True si es válido, False en caso contrario.
    """
    if not isinstance(isbn, str):
        return False
    if len(isbn) != 13 or not isbn.isdigit():
        return False

    # Algoritmo ISBN-13
    total = 0
    for i, digito_char in enumerate(isbn[:12]):
        digito = int(digito_char)
        if i % 2 == 0:
            total += digito
        else:
            total += digito * 3
    digito_verificador = (10 - (total % 10)) % 10
    return digito_verificador == int(isbn[12])


def validar_email(email: str) -> bool:
    """
    Valida formato básico de email: contiene @ y dominio con punto.
    """
    if "@" not in email:
        return False
    local, dominio = email.split("@", 1)
    if not local or "." not in dominio:
        return False
    return True