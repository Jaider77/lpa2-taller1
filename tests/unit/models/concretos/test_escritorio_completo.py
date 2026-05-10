"""
Pruebas exhaustivas para la clase Escritorio.
"""

import pytest
from src.models.concretos.escritorio import Escritorio


class TestEscritorioBasico:
    """Pruebas básicas de instanciación."""

    def test_crear_escritorio_default(self):
        """Prueba crear un escritorio con parámetros default."""
        escritorio = Escritorio("Escritorio", "Madera", "Nogal", 250.0)
        assert escritorio.nombre == "Escritorio"
        assert escritorio.material == "Madera"
        assert escritorio.color == "Nogal"
        assert escritorio.precio_base == 250.0
        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    def test_crear_escritorio_personalizado(self):
        """Prueba crear un escritorio con parámetros personalizados."""
        escritorio = Escritorio(
            nombre="Escritorio Ejecutivo",
            material="Caoba",
            color="Marrón",
            precio_base=500.0,
            forma="hexagonal",
            tiene_cajones=True,
            num_cajones=3,
            largo=1.8,
            tiene_iluminacion=True,
        )
        assert escritorio.nombre == "Escritorio Ejecutivo"
        assert escritorio.forma == "hexagonal"
        assert escritorio.tiene_cajones is True
        assert escritorio.num_cajones == 3
        assert escritorio.largo == 1.8
        assert escritorio.tiene_iluminacion is True


class TestEscritorioPropiedades:
    """Pruebas para propiedades del escritorio."""

    @pytest.fixture
    def escritorio(self):
        """Fixture para crear un escritorio de prueba."""
        return Escritorio(
            "Escritorio Test",
            "Madera",
            "Nogal",
            300.0,
            forma="rectangular",
            tiene_cajones=True,
            num_cajones=2,
        )

    def test_forma_property(self, escritorio):
        """Prueba la propiedad forma."""
        assert escritorio.forma == "rectangular"
        escritorio.forma = "circular"
        assert escritorio.forma == "circular"

    def test_tiene_cajones_property(self, escritorio):
        """Prueba la propiedad tiene_cajones."""
        assert escritorio.tiene_cajones is True

    def test_num_cajones_property(self, escritorio):
        """Prueba la propiedad num_cajones."""
        assert escritorio.num_cajones == 2
        escritorio.num_cajones = 5
        assert escritorio.num_cajones == 5

    def test_largo_property(self, escritorio):
        """Prueba la propiedad largo."""
        assert escritorio.largo == 1.2
        escritorio.largo = 2.0
        assert escritorio.largo == 2.0

    def test_tiene_iluminacion_property(self, escritorio):
        """Prueba la propiedad tiene_iluminacion."""
        assert escritorio.tiene_iluminacion is False
        escritorio.tiene_iluminacion = True
        assert escritorio.tiene_iluminacion is True


class TestEscritorioPrecio:
    """Pruebas para cálculo de precio."""

    def test_calcular_precio_basico(self):
        """Prueba precio básico sin características."""
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Nogal",
            250.0,
            tiene_cajones=False,
            largo=1.2,
            tiene_iluminacion=False,
            forma="rectangular",
        )
        precio = escritorio.calcular_precio()
        assert precio == 250

    def test_calcular_precio_con_cajones(self):
        """Prueba que cada cajón agrega 25 al precio."""
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Nogal",
            250.0,
            tiene_cajones=True,
            num_cajones=3,
        )
        # 250 + (3 * 25) = 325
        precio = escritorio.calcular_precio()
        assert precio == 325

    def test_calcular_precio_con_largo_grande(self):
        """Prueba que largo > 1.5 agrega 50 al precio."""
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Nogal",
            250.0,
            largo=1.8,
            tiene_cajones=False,
        )
        # 250 + 50 = 300
        precio = escritorio.calcular_precio()
        assert precio == 300

    def test_calcular_precio_con_iluminacion(self):
        """Prueba que iluminación agrega 40 al precio."""
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Nogal",
            250.0,
            tiene_iluminacion=True,
            tiene_cajones=False,
        )
        # 250 + 40 = 290
        precio = escritorio.calcular_precio()
        assert precio == 290

    def test_calcular_precio_con_forma_no_rectangular(self):
        """Prueba que forma no rectangular agrega 30 al precio."""
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Nogal",
            250.0,
            forma="ovalada",
            tiene_cajones=False,
        )
        # 250 + 30 = 280
        precio = escritorio.calcular_precio()
        assert precio == 280

    def test_calcular_precio_con_todas_características(self):
        """Prueba precio con todas las características."""
        escritorio = Escritorio(
            "Escritorio Premium",
            "Caoba",
            "Marrón",
            500.0,
            forma="hexagonal",
            tiene_cajones=True,
            num_cajones=4,
            largo=1.9,
            tiene_iluminacion=True,
        )
        # 500 + (4*25) + 50 + 40 + 30 = 720
        precio = escritorio.calcular_precio()
        assert precio == 720


class TestEscritorioDescripcion:
    """Pruebas para descripción."""

    def test_obtener_descripcion_basica(self):
        """Prueba descripción básica."""
        escritorio = Escritorio("Escritorio", "Madera", "Nogal", 250.0)
        desc = escritorio.obtener_descripcion()
        assert "Escritorio" in desc
        assert "Madera" in desc
        assert "Nogal" in desc
        assert isinstance(desc, str)

    def test_obtener_descripcion_con_características(self):
        """Prueba descripción con características."""
        escritorio = Escritorio(
            "Escritorio Ejecutivo",
            "Caoba",
            "Marrón",
            500.0,
            forma="hexagonal",
            tiene_cajones=True,
            num_cajones=3,
            largo=1.8,
            tiene_iluminacion=True,
        )
        desc = escritorio.obtener_descripcion()
        assert "Escritorio Ejecutivo" in desc
        assert "hexagonal" in desc
        assert "1.8" in desc
        assert len(desc) > 0
