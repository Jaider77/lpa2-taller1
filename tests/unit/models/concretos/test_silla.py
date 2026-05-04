"""
Pruebas unitarias para la clase Silla (clase concreta).

Conceptos probados:
- Verificar que Silla se instancia correctamente
- Herencia: que hereda propiedades de Asiento y Mueble
- Propiedades específicas: altura_regulable, tiene_ruedas
- Cálculo de precio
- Descripción
"""

import pytest
from src.models.concretos.silla import Silla


class TestSillaInstanciacion:
    """Pruebas para la instanciación de Silla."""

    def test_crear_silla_basica(self):
        """Prueba crear una silla con parámetros mínimos."""
        silla = Silla(
            nombre="Silla Básica",
            material="Madera",
            color="Rojo",
            precio_base=50.0
        )
        
        assert silla.nombre == "Silla Básica"
        assert silla.material == "Madera"
        assert silla.color == "Rojo"
        assert silla.precio_base == 50.0

    def test_crear_silla_completa(self):
        """Prueba crear una silla con todos los parámetros."""
        silla = Silla(
            nombre="Silla Gamer",
            material="Cuero",
            color="Negro",
            precio_base=300.0,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            altura_regulable=True,
            tiene_ruedas=True
        )
        
        assert silla.nombre == "Silla Gamer"
        assert silla.altura_regulable is True
        assert silla.tiene_ruedas is True

    def test_silla_siempre_capacidad_uno(self):
        """Prueba que una Silla siempre tiene capacidad de 1 persona."""
        silla = Silla("Silla", "Madera", "Rojo", 50.0)
        assert silla.capacidad_personas == 1


class TestSillaProperties:
    """Pruebas para las propiedades específicas de Silla."""
    
    @pytest.fixture
    def silla_basica(self):
        """Fixture que proporciona una silla básica."""
        return Silla("Silla Básica", "Madera", "Rojo", 50.0)

    def test_altura_regulable_getter(self, silla_basica):
        """Prueba el getter de altura_regulable."""
        assert silla_basica.altura_regulable is False

    def test_altura_regulable_setter(self, silla_basica):
        """Prueba el setter de altura_regulable."""
        silla_basica.altura_regulable = True
        assert silla_basica.altura_regulable is True

    def test_tiene_ruedas_getter(self, silla_basica):
        """Prueba el getter de tiene_ruedas."""
        assert silla_basica.tiene_ruedas is False

    def test_tiene_ruedas_setter(self, silla_basica):
        """Prueba el setter de tiene_ruedas."""
        silla_basica.tiene_ruedas = True
        assert silla_basica.tiene_ruedas is True


class TestSillaHerencia:
    """Pruebas para verificar la herencia correcta."""
    
    @pytest.fixture
    def silla_heredada(self):
        """Fixture que proporciona una silla con atributos heredados."""
        return Silla(
            nombre="Silla Ergonómica",
            material="Cuero",
            color="Negro",
            precio_base=200.0,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            altura_regulable=True,
            tiene_ruedas=False
        )

    def test_hereda_de_asiento(self, silla_heredada):
        """Prueba que Silla hereda de Asiento."""
        from src.models.categorias.asientos import Asiento
        assert isinstance(silla_heredada, Asiento)

    def test_hereda_propiedades_mueble(self, silla_heredada):
        """Prueba que hereda propiedades de Mueble."""
        from src.models.mueble import Mueble
        assert isinstance(silla_heredada, Mueble)
        assert hasattr(silla_heredada, 'nombre')
        assert hasattr(silla_heredada, 'material')
        assert hasattr(silla_heredada, 'color')
        assert hasattr(silla_heredada, 'precio_base')

    def test_hereda_propiedades_asiento(self, silla_heredada):
        """Prueba que hereda propiedades de Asiento."""
        assert hasattr(silla_heredada, 'capacidad_personas')
        assert hasattr(silla_heredada, 'tiene_respaldo')
        assert hasattr(silla_heredada, 'material_tapizado')

    def test_respaldo_heredado(self, silla_heredada):
        """Prueba que silla tiene respaldo heredado de Asiento."""
        assert silla_heredada.tiene_respaldo is True

    def test_material_tapizado_heredado(self, silla_heredada):
        """Prueba que material_tapizado es heredado de Asiento."""
        assert silla_heredada.material_tapizado == "Cuero"


class TestSillaCalcularPrecio:
    """Pruebas para el cálculo del precio de Silla."""

    @pytest.mark.parametrize("altura_regulable,tiene_ruedas,precio_base,esperado", [
        (False, False, 50.0, 55.0),      # Solo respaldo: 50 * 1.1 = 55
        (False, False, 100.0, 110.0),    # Solo respaldo: 100 * 1.1 = 110
        (False, True, 100.0, 115.0),     # Respaldo + ruedas: 100 * 1.15 = 115
        (True, False, 100.0, 120.0),     # Respaldo + altura: 100 * 1.2 = 120
        (True, True, 100.0, 125.0),      # Todo: 100 * 1.25 = 125
    ])
    def test_calcular_precio_con_variaciones(self, altura_regulable, tiene_ruedas, precio_base, esperado):
        """Prueba cálculo de precio con diferentes configuraciones."""
        silla = Silla(
            "Silla", "Madera", "Rojo", precio_base,
            altura_regulable=altura_regulable,
            tiene_ruedas=tiene_ruedas
        )
        precio = silla.calcular_precio()
        assert precio == esperado

    def test_calcular_precio_silla_gamer(self):
        """Prueba el precio de una silla gamer con todas las características."""
        silla = Silla(
            "Silla Gamer",
            "Cuero",
            "Negro",
            300.0,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            altura_regulable=True,
            tiene_ruedas=True
        )
        # 300 * (1.0 + 0.1 respaldo + 0.2 cuero + 0.05 altura + 0.1 ruedas)
        # 300 * 1.45 = 435
        precio = silla.calcular_precio()
        assert precio == 435.0


class TestSillaObtenerDescripcion:
    """Pruebas para el método obtener_descripcion de Silla."""

    def test_obtener_descripcion_basica(self):
        """Prueba la descripción de una silla básica."""
        silla = Silla("Silla Básica", "Madera", "Rojo", 50.0)
        descripcion = silla.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion

    def test_obtener_descripcion_incluye_caracteristicas(self):
        """Prueba que la descripción incluye características especiales."""
        silla = Silla(
            "Silla Gamer",
            "Cuero",
            "Negro",
            300.0,
            altura_regulable=True,
            tiene_ruedas=True
        )
        descripcion = silla.obtener_descripcion()
        
        assert "Silla Gamer" in descripcion
        # Verificar que mencionacaracterísticas
        assert "regulable" in descripcion.lower() or "ruedas" in descripcion.lower() or \
               "altura" in descripcion.lower() or "altura" in descripcion.lower()
