"""
Pruebas exhaustivas para la clase abstracta Superficie.
"""

import pytest 
from abc import ABC
from src.models.categorias.superficies import Superficie


class TestSuperficieAbstracto:
    """Pruebas para verificar que Superficie es abstracta."""

    def test_superficie_es_abstracta(self):
        """Prueba que Superficie no se puede instanciar directamente."""
        with pytest.raises(TypeError):
            Superficie(
                "Superficie", "Madera", "Nogal", 200.0, 100.0, 50.0, 75.0
            )

    def test_superficie_hereda_de_abc(self):
        """Prueba que Superficie hereda de ABC."""
        assert issubclass(Superficie, ABC)

    def test_superficie_tiene_metodos_abstractos(self):
        """Prueba que Superficie tiene métodos abstractos."""
        assert hasattr(Superficie, "calcular_precio")
        assert hasattr(Superficie, "obtener_descripcion")
        assert Superficie.calcular_precio.__isabstractmethod__
        assert Superficie.obtener_descripcion.__isabstractmethod__


class TestSuperficiePropiedades:
    """Pruebas para las propiedades de una clase concreta derivada."""

    @pytest.fixture
    def superficie_concreta(self):
        """Fixture que proporciona una clase concreta de Superficie."""

        class SuperficieConcreta(Superficie):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_tamaño()

            def obtener_descripcion(self) -> str:
                return f"Superficie: {self.nombre}"

        return SuperficieConcreta(
            "Superficie Test", "Madera", "Nogal", 200.0, 120.0, 80.0, 90.0
        )

    def test_largo_getter(self, superficie_concreta):
        """Prueba getter de largo."""
        assert superficie_concreta.largo == 120.0

    def test_largo_setter_valido(self, superficie_concreta):
        """Prueba setter de largo con valor válido."""
        superficie_concreta.largo = 150.0
        assert superficie_concreta.largo == 150.0

    def test_largo_setter_cero_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza cero."""
        with pytest.raises(ValueError, match="El largo debe ser mayor a 0"):
            superficie_concreta.largo = 0

    def test_largo_setter_negativo_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza negativos."""
        with pytest.raises(ValueError, match="El largo debe ser mayor a 0"):
            superficie_concreta.largo = -10

    def test_ancho_getter(self, superficie_concreta):
        """Prueba getter de ancho."""
        assert superficie_concreta.ancho == 80.0

    def test_ancho_setter_valido(self, superficie_concreta):
        """Prueba setter de ancho con valor válido."""
        superficie_concreta.ancho = 100.0
        assert superficie_concreta.ancho == 100.0

    def test_ancho_setter_cero_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza cero."""
        with pytest.raises(ValueError, match="El ancho debe ser mayor a 0"):
            superficie_concreta.ancho = 0

    def test_ancho_setter_negativo_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza negativos."""
        with pytest.raises(ValueError, match="El ancho debe ser mayor a 0"):
            superficie_concreta.ancho = -5

    def test_altura_getter(self, superficie_concreta):
        """Prueba getter de altura."""
        assert superficie_concreta.altura == 90.0

    def test_altura_setter_valido(self, superficie_concreta):
        """Prueba setter de altura con valor válido."""
        superficie_concreta.altura = 95.0
        assert superficie_concreta.altura == 95.0

    def test_altura_setter_cero_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza cero."""
        with pytest.raises(ValueError, match="La altura debe ser mayor a 0"):
            superficie_concreta.altura = 0

    def test_altura_setter_negativo_lanza_error(self, superficie_concreta):
        """Prueba que setter rechaza negativos."""
        with pytest.raises(ValueError, match="La altura debe ser mayor a 0"):
            superficie_concreta.altura = -1


class TestSuperficieMetodos:
    """Pruebas para métodos específicos de Superficie."""

    @pytest.fixture
    def superficie_concreta(self):
        """Fixture con superficie concreta."""

        class SuperficieConcreta(Superficie):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_tamaño()

            def obtener_descripcion(self) -> str:
                return f"Superficie: {self.nombre}"

        return SuperficieConcreta(
            "Superficie Test", "Madera", "Nogal", 200.0, 100.0, 50.0, 75.0
        )

    def test_calcular_area(self, superficie_concreta):
        """Prueba cálculo del área."""
        expected_area = 100.0 * 50.0  # largo * ancho
        assert superficie_concreta.calcular_area() == expected_area

    def test_calcular_factor_tamaño_pequeno(self, superficie_concreta):
        """Prueba factor de tamaño para área pequeña."""
        # Área = 100 * 50 = 5000 cm²
        # Factor = 1.0 + (5000 / 10000) * 0.05 = 1.0 + 0.025 = 1.025
        expected_factor = 1.025
        assert superficie_concreta.calcular_factor_tamaño() == pytest.approx(expected_factor)

    def test_calcular_factor_tamaño_grande(self):
        """Prueba factor de tamaño para área grande."""
        class SuperficieConcreta(Superficie):
            def calcular_precio(self) -> float:
                return self.precio_base

            def obtener_descripcion(self) -> str:
                return "Test"

        superficie = SuperficieConcreta("Grande", "Madera", "Nogal", 200.0, 200.0, 100.0, 75.0)
        # Área = 200 * 100 = 20000 cm²
        # Factor = 1.0 + (20000 / 10000) * 0.05 = 1.0 + 0.1 = 1.1
        expected_factor = 1.1
        assert superficie.calcular_factor_tamaño() == pytest.approx(expected_factor)

    def test_obtener_info_superficie(self, superficie_concreta):
        """Prueba obtener información de superficie."""
        info = superficie_concreta.obtener_info_superficie()
        expected = "Dimensiones: 100.0x50.0x75.0cm (Área: 5000.0cm²)"
        assert info == expected