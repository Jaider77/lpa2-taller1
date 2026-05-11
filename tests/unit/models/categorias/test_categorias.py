"""
Pruebas unitarias para las categorías (Almacenamiento y Superficies).
"""

import pytest
from src.models.categorias.almacenamiento import Almacenamiento
from src.models.categorias.superficies import Superficie


class TestAlmacenamientoAbstracta:
    """Pruebas para la clase abstracta Almacenamiento."""

    def test_almacenamiento_es_abstracta(self):
        """Prueba que Almacenamiento no se puede instanciar."""
        with pytest.raises(TypeError):
            Almacenamiento(
                "Armario", "Madera", "Rojo", 200.0,
                capacidad_litros=100.0, tiene_puertas=True
            )


class TestSuperficieAbstracta:
    """Pruebas para la clase abstracta Superficie."""

    def test_superficie_es_abstracta(self):
        """Prueba que Superficie no se puede instanciar."""
        with pytest.raises(TypeError):
            Superficie(
                "Mesa", "Madera", "Rojo", 100.0,
                largo=120.0, ancho=80.0, altura=75.0
            )

    @pytest.fixture
    def superficie_concreta(self):
        """Fixture que proporciona una clase concreta de Superficie."""
        from src.models.concretos.mesa import Mesa
        return Mesa("Mesa", "Madera", "Rojo", 100.0, largo=150.0, ancho=80.0)

    def test_superficie_propiedades_dimensiones(self, superficie_concreta):
        """Prueba que Superficie tiene propiedades de dimensiones."""
        assert hasattr(superficie_concreta, 'largo')
        assert hasattr(superficie_concreta, 'ancho')
        assert hasattr(superficie_concreta, 'altura')
        assert superficie_concreta.largo == 150.0
        assert superficie_concreta.ancho == 80.0

    def test_calcular_area(self, superficie_concreta):
        """Prueba el método calcular_area."""
        if hasattr(superficie_concreta, 'calcular_area'):
            area = superficie_concreta.calcular_area()
            # Area = largo * ancho = 150 * 80 = 12000
            assert area == 150.0 * 80.0
