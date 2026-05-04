# Sistema de Gestión de Biblioteca Digital (SGBD)

## Descripción
Este proyecto es un sistema de gestión de biblioteca desarrollado en Python.
Permite administrar libros, usuarios y préstamos aplicando Programación Orientada a Objetos (POO), colecciones y persistencia en JSON.

Incluye:
- Aplicación de consola (main.py)
- Interfaz gráfica tipo aplicación (MiExamen.py)

---

## Tecnologías usadas
- Python 3.10+
- VS Code
- Programación Orientada a Objetos (POO)
- Tkinter (interfaz gráfica)
- JSON (persistencia de datos)

---

## Estructura del proyecto

SGBD_HIJ/
│
├── main.py
├── MiExamen.py
│
├── modelos/
├── servicios/
├── utils/
├── datos/
│
├── README.md
├── prompts_log.md

---

## Cómo ejecutar

Modo consola (requerido por el examen):
py main.py

Modo interfaz gráfica:
py MiExamen.py

---

## Funcionalidades

- Agregar, buscar y eliminar libros
- Registrar usuarios (Alumno, Profesor, Administrador)
- Registrar préstamos y devoluciones
- Manejo de cola de espera
- Generación de reportes
- Guardado y carga de datos con JSON

---

## Conceptos aplicados

- Clases y objetos
- Herencia
- Polimorfismo
- Encapsulamiento
- Clases abstractas (ABC)
- Protocolos (Protocol)
- Colecciones (list, dict, deque, Counter, defaultdict)
- Manejo de strings
- Control de flujo (if, match/case)
- Persistencia con archivos JSON

---

## Uso de IA

Se utilizó una inteligencia artificial como apoyo para:
- Generación de código base
- Corrección de errores
- Explicación de conceptos

El detalle completo se encuentra en el archivo:
prompts_log.md

---

## Notas

- main.py cumple con los requisitos del examen (menú de consola).
- MiExamen.py es una versión visual adicional.
- Los datos se guardan en:
datos/biblioteca.json


##  Resumen de cumplimiento de la rúbrica

| Criterio           | Estado                       |
|--------------------|------------------------------|
| Type hints         |  Implementados               |
| Docstrings         |  En clases principales       |
| PEP 8              |  Nombres y estructura        |
| Encapsulamiento    |  Uso de @property            |
| Herencia           |  Libros y usuarios           |
| Polimorfismo       |  Métodos como mostrar_info() |
| Protocolo Buscable |  En Catalogo                 |
| Colecciones        |  deque, Counter, defaultdict |
| Persistencia JSON  |  Guardado y carga            |
| Menú y control     |  match/case y try/except     |
| Datos de prueba    |  Incluidos                   |
| Manejo de errores  |  Básico y controlado         |