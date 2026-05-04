"""
conftest.py - Configuración compartida para pruebas unitarias

Este archivo contiene fixtures y configuraciones que se comparten
entre todas las pruebas del proyecto.
"""

import pytest


def pytest_configure(config):
    """Registra marcadores de pruebas personalizados."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
