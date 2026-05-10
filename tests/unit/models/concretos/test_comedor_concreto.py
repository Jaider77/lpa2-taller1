"""
Pruebas exhaustivas para la clase Comedor (concreta).
"""

import pytest
from src.models.concretos.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorBasico:
    """Pruebas básicas de instanciación."""

    @pytest.fixture
    def mesa(self):
        """Fixture para crear una mesa."""
        return Mesa("Mesa Comedor", "Madera", "Nogal", 400.0, forma="circular")

    @pytest.fixture
    def silla(self):
        """Fixture para crear una silla."""
        return Silla("Silla", "Tela", "Gris", 100.0)

    def test_crear_comedor_solo_mesa(self, mesa):
        """Prueba crear un comedor solo con mesa."""
        comedor = Comedor(mesa)
        assert comedor.mesa == mesa
        assert comedor.sillas == []
        assert comedor.cantidad_sillas() == 0

    def test_crear_comedor_con_sillas(self, mesa, silla):
        """Prueba crear un comedor con mesa y sillas."""
        sillas = [silla]
        comedor = Comedor(mesa, sillas)
        assert comedor.mesa == mesa
        assert len(comedor.sillas) == 1
        assert comedor.cantidad_sillas() == 1

    def test_crear_comedor_con_múltiples_sillas(self, mesa, silla):
        """Prueba crear un comedor con varias sillas."""
        sillas = [silla, silla, silla, silla]
        comedor = Comedor(mesa, sillas)
        assert comedor.cantidad_sillas() == 4


class TestComedorSillas:
    """Pruebas para agregar y quitar sillas."""

    @pytest.fixture
    def comedor_setup(self):
        """Fixture para crear un comedor de prueba."""
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0)
        return Comedor(mesa)

    def test_agregar_silla(self, comedor_setup):
        """Prueba agregar una silla."""
        silla = Silla("Silla", "Tela", "Gris", 100.0)
        comedor_setup.agregar_silla(silla)
        assert comedor_setup.cantidad_sillas() == 1
        assert silla in comedor_setup.sillas

    def test_agregar_múltiples_sillas(self, comedor_setup):
        """Prueba agregar varias sillas."""
        sillas = [Silla(f"Silla {i}", "Tela", "Gris", 100.0) for i in range(4)]
        for silla in sillas:
            comedor_setup.agregar_silla(silla)
        assert comedor_setup.cantidad_sillas() == 4

    def test_quitar_silla(self, comedor_setup):
        """Prueba quitar una silla existente."""
        silla1 = Silla("Silla 1", "Tela", "Gris", 100.0)
        silla2 = Silla("Silla 2", "Tela", "Azul", 100.0)
        comedor_setup.agregar_silla(silla1)
        comedor_setup.agregar_silla(silla2)
        assert comedor_setup.cantidad_sillas() == 2

        comedor_setup.quitar_silla(silla1)
        assert comedor_setup.cantidad_sillas() == 1
        assert silla1 not in comedor_setup.sillas
        assert silla2 in comedor_setup.sillas

    def test_quitar_silla_no_existente(self, comedor_setup):
        """Prueba quitar una silla que no existe."""
        silla1 = Silla("Silla 1", "Tela", "Gris", 100.0)
        silla2 = Silla("Silla 2", "Tela", "Azul", 100.0)
        comedor_setup.agregar_silla(silla1)

        # No debería fallar
        comedor_setup.quitar_silla(silla2)
        assert comedor_setup.cantidad_sillas() == 1


class TestComedorPrecio:
    """Pruebas para cálculo de precio total."""

    def test_calcular_precio_solo_mesa(self):
        """Prueba cálculo de precio con solo mesa."""
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0, forma="cuadrada")
        comedor = Comedor(mesa)
        precio = comedor.calcular_precio()
        assert precio > 0
        assert precio == mesa.calcular_precio()

    def test_calcular_precio_con_sillas(self):
        """Prueba cálculo de precio incluye sillas."""
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0, forma="rectangular")
        silla = Silla("Silla", "Tela", "Gris", 100.0)
        comedor = Comedor(mesa, [silla])

        precio = comedor.calcular_precio()
        precio_esperado = mesa.calcular_precio() + silla.calcular_precio()
        assert precio == precio_esperado

    def test_calcular_precio_con_múltiples_sillas(self):
        """Prueba cálculo de precio con varias sillas."""
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0, forma="ovalada")
        sillas = [Silla("Silla", "Tela", "Gris", 100.0) for _ in range(4)]
        comedor = Comedor(mesa, sillas)

        precio = comedor.calcular_precio()
        precio_esperado = mesa.calcular_precio() + sum(
            silla.calcular_precio() for silla in sillas
        )
        assert precio == precio_esperado

    def test_calcular_precio_después_agregar_silla(self):
        """Prueba que el precio se actualiza al agregar silla."""
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0)
        comedor = Comedor(mesa)
        precio_inicial = comedor.calcular_precio()

        silla = Silla("Silla", "Tela", "Gris", 100.0)
        comedor.agregar_silla(silla)
        precio_final = comedor.calcular_precio()

        assert precio_final > precio_inicial


class TestComedorDescripcion:
    """Pruebas para descripción."""

    def test_descripcion_comedor_vacío(self):
        """Prueba descripción de comedor sin sillas."""
        mesa = Mesa("Mesa Comedor", "Madera", "Nogal", 400.0)
        comedor = Comedor(mesa)
        desc = comedor.descripcion()
        assert isinstance(desc, str)
        assert "Comedor" in desc
        assert "Mesa Comedor" in desc
        assert "0 sillas" in desc

    def test_descripcion_comedor_con_sillas(self):
        """Prueba descripción de comedor con sillas."""
        mesa = Mesa("Mesa Comedor", "Madera", "Nogal", 400.0)
        silla1 = Silla("Silla 1", "Tela", "Gris", 100.0)
        silla2 = Silla("Silla 2", "Tela", "Azul", 100.0)
        comedor = Comedor(mesa, [silla1, silla2])

        desc = comedor.descripcion()
        assert isinstance(desc, str)
        assert "Comedor" in desc
        assert "2 sillas" in desc
        assert "Mesa Comedor" in desc
