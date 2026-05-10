"""
Pruebas exhaustivas para la clase Sofá.
"""

import pytest
from src.models.concretos.sofa import Sofa


class TestSofaBasico:
    """Pruebas básicas de instanciación."""

    def test_crear_sofa_default(self):
        """Prueba crear un sofá con parámetros default."""
        sofa = Sofa("Sofá", "Tela", "Gris", 800.0)
        assert sofa.nombre == "Sofá"
        assert sofa.material == "Tela"
        assert sofa.color == "Gris"
        assert sofa.precio_base == 800.0

    def test_crear_sofa_personalizado(self):
        """Prueba crear un sofá personalizado."""
        sofa = Sofa(
            nombre="Sofá Premium",
            material="Cuero",
            color="Negro",
            precio_base=1200.0,
            capacidad_personas=4,
            material_tapizado="Cuero",
            es_modular=True,
            incluye_cojines=True,
        )
        assert sofa.nombre == "Sofá Premium"
        assert sofa.capacidad_personas == 4


class TestSofaPropiedades:
    """Pruebas para propiedades del sofá."""

    @pytest.fixture
    def sofa(self):
        """Fixture para crear un sofá de prueba."""
        return Sofa(
            "Sofá Test",
            "Tela",
            "Azul",
            900.0,
            capacidad_personas=2,
            es_modular=False,
            incluye_cojines=False,
        )

    def test_capacidad_personas(self, sofa):
        """Prueba capacidad de personas."""
        assert sofa.capacidad_personas == 2

    def test_es_modular(self, sofa):
        """Prueba propiedad es_modular."""
        assert sofa.es_modular is False

    def test_incluye_cojines(self, sofa):
        """Prueba propiedad incluye_cojines."""
        assert sofa.incluye_cojines is False


class TestSofaPrecio:
    """Pruebas para cálculo de precio."""

    def test_calcular_precio_basico(self):
        """Prueba cálculo de precio básico."""
        sofa = Sofa(
            "Sofá",
            "Tela",
            "Gris",
            800.0,
            es_modular=False,
            incluye_cojines=False,
        )
        precio = sofa.calcular_precio()
        assert precio > 0
        assert isinstance(precio, (int, float))

    def test_calcular_precio_con_modular(self):
        """Prueba que es_modular afecta el precio."""
        sofa1 = Sofa("Sofá", "Tela", "Gris", 800.0, es_modular=True)
        sofa2 = Sofa("Sofá", "Tela", "Gris", 800.0, es_modular=False)
        precio1 = sofa1.calcular_precio()
        precio2 = sofa2.calcular_precio()
        assert precio1 > precio2

    def test_calcular_precio_con_cojines(self):
        """Prueba que incluye_cojines afecta el precio."""
        sofa1 = Sofa(
            "Sofá",
            "Tela",
            "Gris",
            800.0,
            incluye_cojines=True,
        )
        sofa2 = Sofa(
            "Sofá",
            "Tela",
            "Gris",
            800.0,
            incluye_cojines=False,
        )
        precio1 = sofa1.calcular_precio()
        precio2 = sofa2.calcular_precio()
        assert precio1 > precio2


class TestSofaDescripcion:
    """Pruebas para descripción."""

    def test_obtener_descripcion_basica(self):
        """Prueba descripción básica."""
        sofa = Sofa("Sofá", "Tela", "Gris", 800.0)
        desc = sofa.obtener_descripcion()
        assert isinstance(desc, str)
        assert "Sofá" in desc

    def test_obtener_descripcion_con_características(self):
        """Prueba descripción con características."""
        sofa = Sofa(
            "Sofá Premium",
            "Cuero",
            "Negro",
            1200.0,
            capacidad_personas=3,
            es_modular=True,
            incluye_cojines=True,
        )
        desc = sofa.obtener_descripcion()
        assert isinstance(desc, str)
        assert len(desc) > 0
