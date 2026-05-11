"""
Pruebas unitarias para clases concretas adicionales.
"""

from src.models.concretos.sillon import Sillon
from src.models.concretos.cajonera import Cajonera
from src.models.concretos.escritorio import Escritorio


class TestSillonInstanciacion:
    """Pruebas para la instanciación de Sillón."""

    def test_crear_sillon_basico(self):
        """Prueba crear un sillón básico."""
        sillon = Sillon("Sillón Relax", "Tela", "Gris", 400.0)
        assert sillon.nombre == "Sillón Relax"
        assert sillon.precio_base == 400.0

    def test_sillon_tiene_capacidad_uno(self):
        """Prueba que sillón tiene capacidad de 1."""
        sillon = Sillon("Sillón", "Tela", "Gris", 400.0)
        assert sillon.capacidad_personas == 1


class TestCajoneraInstanciacion:
    """Pruebas para la instanciación de Cajonera."""

    def test_crear_cajonera_basica(self):
        """Prueba crear una cajonera básica."""
        cajonera = Cajonera("Cajonera", "MDF", "Blanco", 150.0)
        assert cajonera.nombre == "Cajonera"
        assert cajonera.precio_base == 150.0

    def test_cajonera_calcular_precio(self):
        """Prueba cálculo de precio de cajonera."""
        cajonera = Cajonera("Cajonera", "MDF", "Blanco", 150.0, num_cajones=5)
        precio = cajonera.calcular_precio()
        assert precio > 0


class TestEscritorioInstanciacion:
    """Pruebas para la instanciación de Escritorio."""

    def test_crear_escritorio_basico(self):
        """Prueba crear un escritorio básico."""
        escritorio = Escritorio("Escritorio", "Madera", "Nogal", 250.0)
        assert escritorio.nombre == "Escritorio"
        assert escritorio.precio_base == 250.0

    def test_escritorio_calcular_precio(self):
        """Prueba cálculo de precio de escritorio."""
        escritorio = Escritorio(
            "Escritorio Ejecutivo",
            "Madera",
            "Nogal",
            500.0,
            capacidad_personas=1
        )
        precio = escritorio.calcular_precio()
        assert precio > 0
