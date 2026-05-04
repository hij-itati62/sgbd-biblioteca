"""Funciones de manipulación de strings."""
import unicodedata
import re


def normalizar_titulo(titulo: str) -> str:
    """
    Capitaliza cada palabra, elimina espacios extra y caracteres especiales.

    Args:
        titulo: Título original.

    Returns:
        Título normalizado.
    """
    # Eliminar espacios múltiples
    titulo = " ".join(titulo.split())
    # Capitalizar título
    titulo = titulo.title()
    # Eliminar caracteres no letras/números/espacios/comas
    titulo = re.sub(r"[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\s,]", "", titulo)
    return titulo


def generar_slug(texto: str) -> str:
    """
    Convierte texto a formato slug URL (minúsculas, guiones, sin acentos).

    Args:
        texto: Texto a convertir.

    Returns:
        Slug URL.
    """
    # Normalizar Unicode: eliminar acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    # Minúsculas y reemplazar espacios por guiones
    slug = texto.lower().replace(" ", "-")
    # Eliminar caracteres no alfanuméricos o guiones
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug


def formatear_reporte_libro(libro_dict: dict) -> str:
    """
    Genera cadena multilínea con f-strings y alineación.

    Args:
        libro_dict: Diccionario con datos del libro.

    Returns:
        Reporte formateado.
    """
    titulo = libro_dict.get("titulo", "Sin título")
    autor = libro_dict.get("autor", "Anónimo")
    isbn = libro_dict.get("isbn", "N/A")
    disponible = "Sí" if libro_dict.get("disponible", False) else "No"

    return f"""
    📖 Título: {titulo:<30}
    ✍️  Autor : {autor:<30}
    🔢 ISBN  : {isbn:<13}
    🟢 Disponible: {disponible}
    """


def buscar_en_texto(haystack: str, needle: str) -> bool:
    """
    Búsqueda case-insensitive usando métodos de string.

    Args:
        haystack: Texto donde buscar.
        needle: Texto a buscar.

    Returns:
        True si encuentra, False en caso contrario.
    """
    return needle.lower() in haystack.lower()