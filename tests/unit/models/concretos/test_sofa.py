"""
Pruebas unitarias para la clase Sofá (clase concreta).
"""

import pytest
from src.models.concretos.sofa import Sofa


class TestSofaInstanciacion:
    """Pruebas para la instanciación de Sofá."""

    def test_crear_sofa_basica(self):
        """Prueba crear un sofá con parámetros mínimos."""
        sofa = Sofa("Sofá Familiar", "Tela", "Gris", 500.0)
        assert sofa.nombre == "Sofá Familiar"
        assert sofa.precio_base == 500.0

    def test_crear_sofa_completa(self):
        """Prueba crear un sofá con todos los parámetros."""
        sofa = Sofa(
            "Sofá Modular",
            "Cuero",
            "Negro",
            1000.0,
            capacidad_personas=4,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            tiene_brazos=True,
            es_modular=True,
            incluye_cojines=True
        )
        assert sofa.capacidad_personas == 4
        assert sofa.es_modular is True
        assert sofa.incluye_cojines is True


class TestSofaProperties:
    """Pruebas para las propiedades específicas de Sofá."""
    
    @pytest.fixture
    def sofa_basica(self):
        return Sofa("Sofá", "Tela", "Gris", 500.0)

    def test_tiene_brazos_getter(self, sofa_basica):
        """Prueba getter de tiene_brazos."""
        assert sofa_basica.tiene_brazos is True

    def test_es_modular_getter(self, sofa_basica):
        """Prueba getter de es_modular."""
        assert sofa_basica.es_modular is False

    def test_incluye_cojines_getter(self, sofa_basica):
        """Prueba getter de incluye_cojines."""
        assert sofa_basica.incluye_cojines is False


class TestSofaCalcularPrecio:
    """Pruebas para el cálculo del precio."""

    def test_calcular_precio_basico(self):
        """Prueba cálculo de precio de sofá básico."""
        sofa = Sofa("Sofá", "Tela", "Gris", 500.0)
        precio = sofa.calcular_precio()
        assert precio > 0

    def test_precio_modular_mayor(self):
        """Prueba que sofá modular cuesta más."""
        sofa_normal = Sofa("Sofá", "Tela", "Gris", 500.0, es_modular=False)
        sofa_modular = Sofa("Sofá", "Tela", "Gris", 500.0, es_modular=True)
        
        precio_normal = sofa_normal.calcular_precio()
        precio_modular = sofa_modular.calcular_precio()
        
        assert precio_modular > precio_normal

    def test_precio_con_cojines_mayor(self):
        """Prueba que sofá con cojines cuesta más."""
        sofa_sin = Sofa("Sofá", "Tela", "Gris", 500.0, incluye_cojines=False)
        sofa_con = Sofa("Sofá", "Tela", "Gris", 500.0, incluye_cojines=True)
        
        precio_sin = sofa_sin.calcular_precio()
        precio_con = sofa_con.calcular_precio()
        
        assert precio_con > precio_sin


class TestSofaHerencia:
    """Pruebas para verificar la herencia."""

    def test_hereda_de_asiento(self):
        """Prueba que Sofá hereda de Asiento."""
        from src.models.categorias.asientos import Asiento
        sofa = Sofa("Sofá", "Tela", "Gris", 500.0)
        assert isinstance(sofa, Asiento)

    def test_hereda_de_mueble(self):
        """Prueba que Sofá hereda de Mueble."""
        from src.models.mueble import Mueble
        sofa = Sofa("Sofá", "Tela", "Gris", 500.0)
        assert isinstance(sofa, Mueble)
