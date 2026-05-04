"""
Pruebas unitarias para la clase abstracta Asiento.

Conceptos probados:
- Verificar que Asiento es abstracta
- Probar getters y setters de asientos
- Probar el cálculo del factor de comodidad
"""

import pytest
from abc import ABC
from src.models.categorias.asientos import Asiento


class TestAsientoAbstracta:
    """Pruebas para verificar que Asiento es una clase abstracta."""

    def test_asiento_es_abstracta(self):
        """Verifica que Asiento no se puede instanciar directamente."""
        with pytest.raises(TypeError):
            asiento = Asiento("Silla", "Madera", "Rojo", 100.0, 1, True)

    def test_asiento_hereda_de_abc(self):
        """Verifica que Asiento hereda de ABC."""
        assert issubclass(Asiento, ABC)


class TestAsientoProperties:
    """Pruebas para los getters y setters de Asiento."""
    
    @pytest.fixture
    def asiento_concreto(self):
        """Fixture que proporciona una clase concreta de Asiento."""
        class AsientoConcreto(Asiento):
            def calcular_precio(self):
                return self.precio_base * self.calcular_factor_comodidad()
            
            def obtener_descripcion(self):
                return f"{self.nombre} - Capacidad: {self.capacidad_personas}"
        
        return AsientoConcreto(
            nombre="Silla",
            material="Madera",
            color="Rojo",
            precio_base=100.0,
            capacidad_personas=1,
            tiene_respaldo=True,
            material_tapizado="Tela"
        )

    def test_capacidad_personas_getter(self, asiento_concreto):
        """Prueba el getter de capacidad_personas."""
        assert asiento_concreto.capacidad_personas == 1

    def test_capacidad_personas_setter_valido(self, asiento_concreto):
        """Prueba el setter de capacidad_personas con valor válido."""
        asiento_concreto.capacidad_personas = 2
        assert asiento_concreto.capacidad_personas == 2

    def test_capacidad_personas_setter_cero_lanza_error(self, asiento_concreto):
        """Prueba que capacidad_personas no puede ser 0."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            asiento_concreto.capacidad_personas = 0

    def test_capacidad_personas_setter_negativo_lanza_error(self, asiento_concreto):
        """Prueba que capacidad_personas no puede ser negativa."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            asiento_concreto.capacidad_personas = -1

    def test_tiene_respaldo_getter(self, asiento_concreto):
        """Prueba el getter de tiene_respaldo."""
        assert asiento_concreto.tiene_respaldo is True

    def test_tiene_respaldo_setter(self, asiento_concreto):
        """Prueba el setter de tiene_respaldo."""
        asiento_concreto.tiene_respaldo = False
        assert asiento_concreto.tiene_respaldo is False

    def test_material_tapizado_getter(self, asiento_concreto):
        """Prueba el getter de material_tapizado."""
        assert asiento_concreto.material_tapizado == "Tela"

    def test_material_tapizado_setter(self, asiento_concreto):
        """Prueba el setter de material_tapizado."""
        asiento_concreto.material_tapizado = "Cuero"
        assert asiento_concreto.material_tapizado == "Cuero"

    def test_material_tapizado_none(self, asiento_concreto):
        """Prueba que material_tapizado puede ser None."""
        asiento_concreto.material_tapizado = None
        assert asiento_concreto.material_tapizado is None


class TestCalcularFactorComodidad:
    """Pruebas para el cálculo del factor de comodidad."""
    
    @pytest.fixture
    def asiento_concreto(self):
        """Fixture que proporciona una clase concreta de Asiento."""
        class AsientoConcreto(Asiento):
            def calcular_precio(self):
                return self.precio_base * self.calcular_factor_comodidad()
            
            def obtener_descripcion(self):
                return f"{self.nombre}"
        
        return AsientoConcreto
    
    def test_factor_comodidad_base_sin_respaldo(self, asiento_concreto):
        """Prueba factor de comodidad sin respaldo."""
        asiento = asiento_concreto(
            "Banqueta", "Madera", "Rojo", 100.0, 1, False, None
        )
        factor = asiento.calcular_factor_comodidad()
        assert factor == 1.0  # Base sin respaldo

    def test_factor_comodidad_con_respaldo(self, asiento_concreto):
        """Prueba factor de comodidad con respaldo."""
        asiento = asiento_concreto(
            "Silla", "Madera", "Rojo", 100.0, 1, True, None
        )
        factor = asiento.calcular_factor_comodidad()
        assert factor == 1.1  # 1.0 + 0.1 por respaldo

    def test_factor_comodidad_con_tapizado_cuero(self, asiento_concreto):
        """Prueba factor de comodidad con tapizado de cuero."""
        asiento = asiento_concreto(
            "Silla", "Madera", "Rojo", 100.0, 1, True, "Cuero"
        )
        factor = asiento.calcular_factor_comodidad()
        assert factor == 1.3  # 1.0 + 0.1 (respaldo) + 0.2 (cuero)

    def test_factor_comodidad_con_tapizado_tela(self, asiento_concreto):
        """Prueba factor de comodidad con tapizado de tela."""
        asiento = asiento_concreto(
            "Silla", "Madera", "Rojo", 100.0, 1, True, "Tela"
        )
        factor = asiento.calcular_factor_comodidad()
        assert factor == 1.2  # 1.0 + 0.1 (respaldo) + 0.1 (tela)

    def test_factor_comodidad_con_capacidad_multiples_personas(self, asiento_concreto):
        """Prueba factor de comodidad con capacidad para más personas."""
        asiento = asiento_concreto(
            "Sofá", "Tela", "Gris", 500.0, 3, True, "Tela"
        )
        # 1.0 + 0.1 (respaldo) + 0.1 (tela) + (3-1)*0.05 (capacidad)
        factor = asiento.calcular_factor_comodidad()
        assert factor == 1.3

    def test_calcular_precio_con_factor_comodidad(self, asiento_concreto):
        """Prueba que el cálculo de precio aplica el factor de comodidad."""
        asiento = asiento_concreto(
            "Silla Gamer", "Cuero", "Negro", 100.0, 1, True, "Cuero"
        )
        precio = asiento.calcular_precio()
        # precio_base=100, factor=1.3 (1.0 + 0.1 + 0.2)
        assert precio == 130.0
