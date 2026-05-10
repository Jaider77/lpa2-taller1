"""
Pruebas exhaustivas para la clase abstracta Almacenamiento.
"""

import pytest
from abc import ABC
from src.models.categorias.almacenamiento import Almacenamiento


class TestAlmacenamientoAbstracto:
    """Pruebas para verificar que Almacenamiento es abstracta."""

    def test_almacenamiento_es_abstracta(self):
        """Prueba que Almacenamiento no se puede instanciar directamente."""
        with pytest.raises(TypeError):
            almacenamiento = Almacenamiento(
                "Almacenamiento", "Madera", "Nogal", 200.0, 3, 200.0
            )

    def test_almacenamiento_hereda_de_abc(self):
        """Prueba que Almacenamiento hereda de ABC."""
        assert issubclass(Almacenamiento, ABC)

    def test_almacenamiento_tiene_métodos_abstractos(self):
        """Prueba que Almacenamiento tiene métodos abstractos."""
        assert hasattr(Almacenamiento, "calcular_precio")
        assert hasattr(Almacenamiento, "obtener_descripcion")
        assert Almacenamiento.calcular_precio.__isabstractmethod__
        assert Almacenamiento.obtener_descripcion.__isabstractmethod__


class TestAlmacenamientoPropiedades:
    """Pruebas para las propiedades de una clase concreta derivada."""

    @pytest.fixture
    def almacenamiento_concreto(self):
        """Fixture que proporciona una clase concreta de Almacenamiento."""

        class AlmacenamientoConcreto(Almacenamiento):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_almacenamiento()

            def obtener_descripcion(self) -> str:
                return f"Almacenamiento: {self.nombre}"

        return AlmacenamientoConcreto(
            "Almacenamiento Test", "Madera", "Nogal", 200.0, 4, 300.0
        )

    def test_num_compartimentos_getter(self, almacenamiento_concreto):
        """Prueba getter de num_compartimentos."""
        assert almacenamiento_concreto.num_compartimentos == 4

    def test_num_compartimentos_setter_valido(self, almacenamiento_concreto):
        """Prueba setter de num_compartimentos con valor válido."""
        almacenamiento_concreto.num_compartimentos = 6
        assert almacenamiento_concreto.num_compartimentos == 6

    def test_num_compartimentos_setter_cero_lanza_error(self, almacenamiento_concreto):
        """Prueba que setter rechaza cero compartimentos."""
        with pytest.raises(ValueError, match="El número de compartimentos debe ser mayor a 0"):
            almacenamiento_concreto.num_compartimentos = 0

    def test_num_compartimentos_setter_negativo_lanza_error(self, almacenamiento_concreto):
        """Prueba que setter rechaza negativos."""
        with pytest.raises(ValueError, match="El número de compartimentos debe ser mayor a 0"):
            almacenamiento_concreto.num_compartimentos = -5

    def test_capacidad_litros_getter(self, almacenamiento_concreto):
        """Prueba getter de capacidad_litros."""
        assert almacenamiento_concreto.capacidad_litros == 300.0

    def test_capacidad_litros_setter_valido(self, almacenamiento_concreto):
        """Prueba setter de capacidad_litros con valor válido."""
        almacenamiento_concreto.capacidad_litros = 500.0
        assert almacenamiento_concreto.capacidad_litros == 500.0

    def test_capacidad_litros_setter_cero_lanza_error(self, almacenamiento_concreto):
        """Prueba que setter rechaza cero litros."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            almacenamiento_concreto.capacidad_litros = 0

    def test_capacidad_litros_setter_negativo_lanza_error(self, almacenamiento_concreto):
        """Prueba que setter rechaza negativos."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            almacenamiento_concreto.capacidad_litros = -100


class TestAlmacenamientoFactor:
    """Pruebas para cálculo del factor de almacenamiento."""

    @pytest.fixture
    def almacenamiento_concreto(self):
        """Fixture con almacenamiento concreto."""

        class AlmacenamientoConcreto(Almacenamiento):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_almacenamiento()

            def obtener_descripcion(self) -> str:
                return f"Almacenamiento: {self.nombre}"

        return AlmacenamientoConcreto

    def test_calcular_factor_base(self, almacenamiento_concreto):
        """Prueba factor base con valores mínimos."""
        obj = almacenamiento_concreto("Test", "Madera", "Nogal", 100.0, 1, 100.0)
        # factor = 1.0 + (1-1)*0.05 + (100/100)*0.02 = 1.0 + 0 + 0.02 = 1.02
        factor = obj.calcular_factor_almacenamiento()
        assert factor == pytest.approx(1.02, rel=0.01)

    def test_calcular_factor_con_compartimentos(self, almacenamiento_concreto):
        """Prueba que compartimentos incrementan el factor."""
        obj1 = almacenamiento_concreto("Test", "Madera", "Nogal", 100.0, 1, 100.0)
        obj2 = almacenamiento_concreto("Test", "Madera", "Nogal", 100.0, 5, 100.0)
        factor1 = obj1.calcular_factor_almacenamiento()
        factor2 = obj2.calcular_factor_almacenamiento()
        # obj2 tiene 4 compartimentos más: + 4*0.05 = 0.20
        assert factor2 > factor1

    def test_calcular_factor_con_capacidad(self, almacenamiento_concreto):
        """Prueba que capacidad incrementa el factor."""
        obj1 = almacenamiento_concreto("Test", "Madera", "Nogal", 100.0, 2, 100.0)
        obj2 = almacenamiento_concreto("Test", "Madera", "Nogal", 100.0, 2, 500.0)
        factor1 = obj1.calcular_factor_almacenamiento()
        factor2 = obj2.calcular_factor_almacenamiento()
        # obj2 tiene 400L más: (500-100)/100 * 0.02 - (100-100)/100 * 0.02
        assert factor2 > factor1


class TestAlmacenamientoInfo:
    """Pruebas para obtener información del almacenamiento."""

    def test_obtener_info_almacenamiento(self):
        """Prueba obtener información del almacenamiento."""

        class AlmacenamientoConcreto(Almacenamiento):
            def calcular_precio(self) -> float:
                return self.precio_base

            def obtener_descripcion(self) -> str:
                return "Test"

        obj = AlmacenamientoConcreto("Test", "Madera", "Nogal", 100.0, 3, 200.0)
        info = obj.obtener_info_almacenamiento()
        assert "Compartimentos: 3" in info
        assert "Capacidad: 200.0L" in info
