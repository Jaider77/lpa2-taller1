"""
Pruebas exhaustivas para la clase Sillón.
"""

import pytest
from src.models.concretos.sillon import Sillon


class TestSillonBasico:
    """Pruebas básicas de instanciación de Sillón."""

    def test_crear_sillon_default(self):
        """Prueba crear un sillón con parámetros default."""
        sillon = Sillon("Sillón Relax", "Tela", "Gris", 400.0)
        assert sillon.nombre == "Sillón Relax"
        assert sillon.material == "Tela"
        assert sillon.color == "Gris"
        assert sillon.precio_base == 400.0
        assert sillon.capacidad_personas == 1
        assert sillon.tiene_respaldo is True

    def test_crear_sillon_con_parametros_completos(self):
        """Prueba crear un sillón con todos los parámetros."""
        sillon = Sillon(
            nombre="Sillón Premium",
            material="Cuero",
            color="Negro",
            precio_base=800.0,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        assert sillon.nombre == "Sillón Premium"
        assert sillon.capacidad_personas == 2
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is True
        assert sillon.tiene_reposapiés is True


class TestSillonPropiedades:
    """Pruebas para las propiedades del Sillón."""

    @pytest.fixture
    def sillon(self):
        """Fixture para crear un sillón de prueba."""
        return Sillon(
            "Sillón Test",
            "Tela",
            "Azul",
            500.0,
            capacidad_personas=1,
            tiene_brazos=True,
            es_reclinable=False,
            tiene_reposapiés=False,
        )

    def test_tiene_brazos_getter(self, sillon):
        """Prueba getter de tiene_brazos."""
        assert sillon.tiene_brazos is True

    def test_tiene_brazos_setter(self, sillon):
        """Prueba setter de tiene_brazos."""
        sillon.tiene_brazos = False
        assert sillon.tiene_brazos is False

    def test_es_reclinable_getter(self, sillon):
        """Prueba getter de es_reclinable."""
        assert sillon.es_reclinable is False

    def test_es_reclinable_setter(self, sillon):
        """Prueba setter de es_reclinable."""
        sillon.es_reclinable = True
        assert sillon.es_reclinable is True

    def test_tiene_reposapiés_getter(self, sillon):
        """Prueba getter de tiene_reposapiés."""
        assert sillon.tiene_reposapiés is False

    def test_tiene_reposapiés_setter(self, sillon):
        """Prueba setter de tiene_reposapiés."""
        sillon.tiene_reposapiés = True
        assert sillon.tiene_reposapiés is True


class TestSillonPrecio:
    """Pruebas para cálculo de precio del Sillón."""

    def test_calcular_precio_basico(self):
        """Prueba cálculo de precio sin características adicionales."""
        sillon = Sillon("Sillón", "Tela", "Gris", 400.0, tiene_brazos=False)
        precio = sillon.calcular_precio()
        assert precio == 400

    def test_calcular_precio_con_brazos(self):
        """Prueba que los brazos agregan 100 al precio."""
        sillon = Sillon("Sillón", "Tela", "Gris", 400.0, tiene_brazos=True)
        precio = sillon.calcular_precio()
        assert precio == 500

    def test_calcular_precio_con_reclinable(self):
        """Prueba que reclinable agrega 250 al precio."""
        sillon = Sillon(
            "Sillón", "Tela", "Gris", 400.0, es_reclinable=True, tiene_brazos=False
        )
        precio = sillon.calcular_precio()
        assert precio == 650

    def test_calcular_precio_con_reposapiés(self):
        """Prueba que reposapiés agrega 80 al precio."""
        sillon = Sillon(
            "Sillón", "Tela", "Gris", 400.0, tiene_reposapiés=True, tiene_brazos=False
        )
        precio = sillon.calcular_precio()
        assert precio == 480

    def test_calcular_precio_con_tapizado_cuero(self):
        """Prueba que tapizado en cuero agrega 200 al precio."""
        sillon = Sillon(
            "Sillón",
            "Tela",
            "Gris",
            400.0,
            material_tapizado="Cuero",
            tiene_brazos=False,
        )
        precio = sillon.calcular_precio()
        assert precio == 600

    def test_calcular_precio_con_todas_características(self):
        """Prueba cálculo con todas las características."""
        sillon = Sillon(
            "Sillón Premium",
            "Cuero",
            "Negro",
            600.0,
            material_tapizado="Cuero",
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        # 600 + 200 (tapizado) + 100 (brazos) + 250 (reclinable) + 80 (reposapiés) = 1230
        precio = sillon.calcular_precio()
        assert precio == 1230


class TestSillonDescripcion:
    """Pruebas para el método obtener_descripcion."""

    def test_obtener_descripcion_basica(self):
        """Prueba descripción de sillón básico."""
        sillon = Sillon("Sillón Relax", "Tela", "Gris", 400.0)
        desc = sillon.obtener_descripcion()
        assert "Sillón Relax" in desc
        assert "Tela" in desc
        assert "Gris" in desc
        assert isinstance(desc, str)
        assert len(desc) > 0

    def test_obtener_descripcion_con_características(self):
        """Prueba descripción incluye características."""
        sillon = Sillon(
            "Sillón Premium",
            "Cuero",
            "Negro",
            800.0,
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        desc = sillon.obtener_descripcion()
        assert isinstance(desc, str)
        assert len(desc) > 0
