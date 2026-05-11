"""
Pruebas exhaustivas para la clase Comedor de composición.
"""

from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorComposicionCompleta:
    """Pruebas para la clase Comedor de composición."""

    def test_crear_comedor_solo_mesa(self):
        mesa = Mesa("Mesa Rectangular", "Madera", "Nogal", 500.0, forma="rectangular")
        comedor = Comedor("Comedor Familiar", mesa)

        assert comedor.nombre == "Comedor Familiar"
        assert comedor.mesa == mesa
        assert len(comedor.sillas) == 0
        assert str(comedor) == "Comedor Comedor Familiar: Mesa + 0 sillas"
        assert len(comedor) == 1

    def test_crear_comedor_con_sillas_iniciales(self):
        mesa = Mesa("Mesa Rectangular", "Madera", "Nogal", 500.0, forma="rectangular")
        sillas = [
            Silla("Silla 1", "Tela", "Gris", 100.0),
            Silla("Silla 2", "Tela", "Azul", 120.0),
        ]
        comedor = Comedor("Comedor Conjunto", mesa, sillas)

        assert len(comedor.sillas) == 2
        assert comedor.sillas == sillas
        assert comedor.obtener_descripcion() == comedor.obtener_descripcion_completa()

    def test_agregar_silla_y_no_perdida_de_referencia(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0, capacidad_personas=4)
        comedor = Comedor("Comedor Test", mesa)

        silla = Silla("Silla", "Tela", "Gris", 100.0)
        resultado = comedor.agregar_silla(silla)

        assert "exitosamente" in resultado.lower()
        assert len(comedor.sillas) == 1
        assert comedor.sillas[0] is silla

    def test_agregar_silla_excede_capacidad_mesa(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0, capacidad_personas=2)
        comedor = Comedor("Comedor Test", mesa)

        comedor.agregar_silla(Silla("Silla 1", "Tela", "Gris", 100.0))
        comedor.agregar_silla(Silla("Silla 2", "Tela", "Gris", 100.0))
        resultado = comedor.agregar_silla(Silla("Silla 3", "Tela", "Gris", 100.0))

        assert "no se pueden agregar" in resultado.lower()
        assert len(comedor.sillas) == 2

    def test_quitar_silla_ultima(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        comedor = Comedor("Comedor Test", mesa, [Silla("Silla 1", "Tela", "Gris", 100.0)])

        resultado = comedor.quitar_silla()

        assert "removida" in resultado.lower()
        assert len(comedor.sillas) == 0

    def test_quitar_silla_indice_invalido(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        comedor = Comedor("Comedor Test", mesa, [Silla("Silla 1", "Tela", "Gris", 100.0)])

        resultado = comedor.quitar_silla(10)

        assert "índice" in resultado.lower()
        assert len(comedor.sillas) == 1

    def test_calcular_precio_total_con_sillas(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0, forma="ovalada")
        sillas = [Silla("Silla", "Tela", "Gris", 100.0) for _ in range(3)]
        comedor = Comedor("Comedor Test", mesa, sillas)

        precio_total = comedor.calcular_precio_total()
        esperado = mesa.calcular_precio() + sum(s.calcular_precio() for s in sillas)

        assert precio_total == esperado

    def test_obtener_descripcion_completa_sin_sillas(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        comedor = Comedor("Comedor Test", mesa)

        descripcion = comedor.obtener_descripcion_completa()

        assert "SILLAS: Ninguna incluida" in descripcion
        assert "PRECIO TOTAL" in descripcion

    def test_obtener_descripcion_completa_con_descuento(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        sillas = [Silla(f"Silla {i}", "Tela", "Gris", 100.0) for i in range(4)]
        comedor = Comedor("Comedor Test", mesa, sillas)

        descripcion = comedor.obtener_descripcion_completa()

        assert "Incluye 5% de descuento" in descripcion
        assert "SILLAS (4 unidades)" in descripcion

    def test_obtener_resumen_incluye_materiales_y_capacidad(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        silla = Silla("Silla", "Tela", "Gris", 100.0)
        comedor = Comedor("Comedor Test", mesa, [silla])

        resumen = comedor.obtener_resumen()

        assert resumen["nombre"] == "Comedor Test"
        assert resumen["total_muebles"] == 2
        assert resumen["capacidad_personas"] == 1
        assert "Madera" in resumen["materiales_utilizados"]

    def test__obtener_materiales_unicos_usa_material_tapizado(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        silla = Silla("Silla", "Cuero", "Rojo", 100.0, material_tapizado="Cuero")
        comedor = Comedor("Comedor Test", mesa, [silla])

        resumen = comedor.obtener_resumen()
        assert "Cuero" in resumen["materiales_utilizados"]

    def test_len_y_str_methods(self):
        mesa = Mesa("Mesa", "Madera", "Nogal", 500.0)
        sillas = [Silla("Silla 1", "Tela", "Gris", 100.0) for _ in range(2)]
        comedor = Comedor("Comedor Test", mesa, sillas)

        assert len(comedor) == 3
        assert "Comedor Comedor Test" in str(comedor)
