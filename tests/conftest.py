"""
conftest.py - Configuración compartida para todas las pruebas

Este archivo contiene fixtures y configuraciones que se comparten
entre todas las pruebas del proyecto.
"""

import os
import sys


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Agregar el directorio src al path para que los imports funcionen
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def pytest_configure(config):
    """Configura marcadores de pruebas y opciones generales."""
    config.addinivalue_line(
        "markers", "integration: marca pruebas de integración"
    )
    config.addinivalue_line(
        "markers", "unit: marca pruebas unitarias"
    )


def pytest_report_header(config):
    """Muestra un encabezado útil al ejecutar pytest."""
    return "Proyecto LPA2 - Pruebas de integración y unitarias"
