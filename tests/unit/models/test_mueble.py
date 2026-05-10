"""
Pruebas unitarias para la clase abstracta Mueble.

Conceptos probados:
- Verificar que Mueble es una clase abstracta
- Verificar que no se puede instanciar directamente
- Probar getters y setters con validaciones
- Probar métodos abstractos
"""

import pytest
from abc import ABC
from src.models.mueble import Mueble


class TestMuebleAbstracto:
    """Grupo de pruebas para verificar que Mueble es abstracta."""

    def test_mueble_es_abstracta(self):
        """
        Verifica que Mueble no se puede instanciar directamente
        porque es una clase abstracta.
        """
        with pytest.raises(TypeError):
            mueble = Mueble("Mesa", "Madera", "Rojo", 100.0)

    def test_mueble_hereda_de_abc(self):
        """Verifica que Mueble hereda de ABC (Abstract Base Class)."""
        assert issubclass(Mueble, ABC)

    def test_mueble_tiene_metodos_abstractos(self):
        """Verifica que Mueble tiene métodos abstractos."""
        assert hasattr(Mueble, 'calcular_precio')
        assert hasattr(Mueble, 'obtener_descripcion')
        
        # Verificar que son abstractos
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__


class TestMuebleProperties:
    """
    Grupo de pruebas para los getters y setters de Mueble.
    
    Nota: Creamos una clase concreta para poder probar
    los atributos de la clase abstracta.
    """
    
    @pytest.fixture
    def mueble_concreto(self):
        """
        Fixture que proporciona una clase concreta de Mueble
        para poder probar sus propiedades.
        """
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            
            def obtener_descripcion(self):
                return f"{self.nombre} - {self.material}"
        
        return MuebleConcreto("Mesa", "Madera", "Rojo", 100.0)

    def test_nombre_getter(self, mueble_concreto):
        """Prueba el getter de nombre."""
        assert mueble_concreto.nombre == "Mesa"

    def test_nombre_setter_valido(self, mueble_concreto):
        """Prueba el setter de nombre con valor válido."""
        mueble_concreto.nombre = "Escritorio"
        assert mueble_concreto.nombre == "Escritorio"

    def test_nombre_setter_vacio_lanza_error(self, mueble_concreto):
        """Prueba que setter de nombre rechaza valores vacíos."""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            mueble_concreto.nombre = ""

    def test_nombre_setter_espacios_en_blanco(self, mueble_concreto):
        """Prueba que setter de nombre rechaza solo espacios."""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            mueble_concreto.nombre = "   "

    def test_nombre_setter_normaliza_espacios(self, mueble_concreto):
        """Prueba que el setter normaliza espacios en blanco."""
        mueble_concreto.nombre = "  Silla  Gamer  "
        assert mueble_concreto.nombre == "Silla Gamer"

    def test_material_getter(self, mueble_concreto):
        """Prueba el getter de material."""
        assert mueble_concreto.material == "Madera"

    def test_material_setter_valido(self, mueble_concreto):
        """Prueba el setter de material con valor válido."""
        mueble_concreto.material = "Metal"
        assert mueble_concreto.material == "Metal"

    def test_material_setter_vacio_lanza_error(self, mueble_concreto):
        """Prueba que setter de material rechaza valores vacíos."""
        with pytest.raises(ValueError, match="El material no puede estar vacío"):
            mueble_concreto.material = ""

    def test_color_getter(self, mueble_concreto):
        """Prueba el getter de color."""
        assert mueble_concreto.color == "Rojo"

    def test_color_setter_valido(self, mueble_concreto):
        """Prueba el setter de color con valor válido."""
        mueble_concreto.color = "Azul"
        assert mueble_concreto.color == "Azul"

    def test_color_setter_vacio_lanza_error(self, mueble_concreto):
        """Prueba que setter de color rechaza valores vacíos."""
        with pytest.raises(ValueError, match="El color no puede estar vacío"):
            mueble_concreto.color = ""

    def test_precio_base_getter(self, mueble_concreto):
        """Prueba el getter de precio_base."""
        assert mueble_concreto.precio_base == 100.0

    def test_precio_base_setter_valido(self, mueble_concreto):
        """Prueba el setter de precio_base con valor válido."""
        mueble_concreto.precio_base = 250.0
        assert mueble_concreto.precio_base == 250.0

    def test_precio_base_setter_cero(self, mueble_concreto):
        """Prueba que setter de precio_base rechaza cero."""
        with pytest.raises(ValueError, match="El precio base debe ser mayor que cero"):
            mueble_concreto.precio_base = 0.0

    def test_precio_base_setter_negativo_lanza_error(self, mueble_concreto):
        """Prueba que setter de precio_base rechaza valores negativos."""
        with pytest.raises(ValueError, match="El precio base no puede ser negativo"):
            mueble_concreto.precio_base = -50.0

    def test_crear_mueble_concreto_con_valores_iniciales(self):
        """Prueba creación de mueble concreto con valores iniciales."""
        class Silla(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        silla = Silla("Silla Gamer", "Cuero", "Negro", 500.0)
        
        assert silla.nombre == "Silla Gamer"
        assert silla.material == "Cuero"
        assert silla.color == "Negro"
        assert silla.precio_base == 500.0


class TestMuebleConstructorValidations:
    """
    Grupo de pruebas para validar que el constructor aplique
    las validaciones de los setters.
    """

    def test_constructor_con_precio_negativo_lanza_error(self):
        """Prueba que constructor rechaza precio negativo."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El precio base debe ser mayor que cero"):
            MuebleConcreto("Mesa", "Madera", "Rojo", -100.0)

    def test_constructor_con_precio_cero_lanza_error(self):
        """Prueba que constructor rechaza precio cero."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El precio base debe ser mayor que cero"):
            MuebleConcreto("Mesa", "Madera", "Rojo", 0.0)

    def test_constructor_con_nombre_vacio_lanza_error(self):
        """Prueba que constructor rechaza nombre vacío."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            MuebleConcreto("", "Madera", "Rojo", 100.0)

    def test_constructor_con_nombre_espacios_lanza_error(self):
        """Prueba que constructor rechaza nombre solo espacios."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            MuebleConcreto("   ", "Madera", "Rojo", 100.0)

    def test_constructor_con_material_vacio_lanza_error(self):
        """Prueba que constructor rechaza material vacío."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El material no puede estar vacío"):
            MuebleConcreto("Mesa", "", "Rojo", 100.0)

    def test_constructor_con_color_vacio_lanza_error(self):
        """Prueba que constructor rechaza color vacío."""
        class MuebleConcreto(Mueble):
            def calcular_precio(self):
                return self.precio_base
            def obtener_descripcion(self):
                return self.nombre
        
        with pytest.raises(ValueError, match="El color no puede estar vacío"):
            MuebleConcreto("Mesa", "Madera", "", 100.0)
