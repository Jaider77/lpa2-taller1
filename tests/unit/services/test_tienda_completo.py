"""
Pruebas exhaustivas adicionales para TiendaMuebles.
"""

import pytest
from src.services.tienda import TiendaMuebles
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla
from src.models.concretos.sofacama import SofaCama
from src.models.composicion.comedor import Comedor


class TestTiendaBusquedaYFiltros:
    """Pruebas para búsqueda y filtros avanzados."""

    @pytest.fixture
    def tienda_poblada(self):
        tienda = TiendaMuebles("Tienda Test")
        tienda.agregar_mueble(Mesa("Mesa 1", "Madera", "Nogal", 400.0))
        tienda.agregar_mueble(Mesa("Mesa 2", "Metal", "Plateado", 350.0))
        tienda.agregar_mueble(Silla("Silla 1", "Tela", "Gris", 100.0))
        tienda.agregar_mueble(Silla("Silla 2", "Cuero", "Negro", 150.0))
        tienda.agregar_mueble(SofaCama("SofaCama 1", "Tela", "Azul", 1200.0))
        return tienda

    def test_buscar_muebles_por_nombre_exacto(self, tienda_poblada):
        resultados = tienda_poblada.buscar_muebles_por_nombre("Mesa 1")
        assert len(resultados) == 1
        assert resultados[0].nombre == "Mesa 1"

    def test_buscar_muebles_por_nombre_parcial(self, tienda_poblada):
        resultados = tienda_poblada.buscar_muebles_por_nombre("Mesa")
        assert len(resultados) == 2

    def test_buscar_por_nombre_alias_retorna_primer_mueble(self, tienda_poblada):
        resultado = tienda_poblada.buscar_por_nombre("Silla")
        assert resultado is not None
        assert "silla" in resultado.nombre.lower()

    def test_filtrar_por_tipo(self, tienda_poblada):
        resultados = tienda_poblada.filtrar_por_tipo("Silla")
        assert len(resultados) == 2
        assert all(type(mueble).__name__ == "Silla" for mueble in resultados)

    def test_filtrar_por_material(self, tienda_poblada):
        resultados = tienda_poblada.filtrar_por_material("Tela")
        assert len(resultados) >= 1
        assert all(mueble.material.lower() == "tela" for mueble in resultados)

    def test_filtrar_por_precio_rango(self, tienda_poblada):
        resultados = tienda_poblada.filtrar_por_precio(100, 400)
        assert len(resultados) >= 1
        for mueble in resultados:
            precio = mueble.calcular_precio()
            assert 100 <= precio <= 400

    def test_obtener_muebles_por_tipo_mesa(self, tienda_poblada):
        resultados = tienda_poblada.obtener_muebles_por_tipo(Mesa)
        assert len(resultados) == 2
        assert all(isinstance(mueble, Mesa) for mueble in resultados)

    def test_buscar_por_nombre_inexistente(self, tienda_poblada):
        resultado = tienda_poblada.buscar_por_nombre("NoExiste")
        assert resultado is None


class TestTiendaDescuentos:
    """Pruebas para gestión de descuentos."""

    @pytest.fixture
    def tienda(self):
        return TiendaMuebles("Tienda Test")

    def test_aplicar_descuento_valido(self, tienda):
        resultado = tienda.aplicar_descuento("Sillas", 0.10)
        assert "descuento" in resultado.lower()
        assert "aplicado" in resultado.lower()

    def test_aplicar_descuento_valido_porcentaje_entero(self, tienda):
        resultado = tienda.aplicar_descuento("Mesas", 15)
        assert "15" in resultado
        assert "aplicado" in resultado.lower()

    def test_aplicar_descuento_negativo_rechazado(self, tienda):
        resultado = tienda.aplicar_descuento("Sillas", -0.10)
        assert "error" in resultado.lower()

    def test_aplicar_descuento_mayor_100_rechazado(self, tienda):
        resultado = tienda.aplicar_descuento("Sillas", 150)
        assert "error" in resultado.lower()

    def test_remover_descuento_existente(self, tienda):
        tienda.aplicar_descuento("Mesas", 0.15)
        resultado = tienda.remover_descuento("Mesas")
        assert "removido" in resultado.lower()

    def test_remover_descuento_inexistente(self, tienda):
        resultado = tienda.remover_descuento("NoExiste")
        assert "no hay descuento aplicado" in resultado.lower()


class TestTiendaVentas:
    """Pruebas para operaciones de venta."""

    @pytest.fixture
    def tienda_vendible(self):
        tienda = TiendaMuebles("Tienda Test")
        tienda.agregar_mueble(Mesa("Mesa Vendible", "Madera", "Nogal", 400.0))
        tienda.agregar_mueble(Silla("Silla Vendible", "Tela", "Gris", 100.0))
        return tienda

    def test_vender_mueble_existente(self, tienda_vendible):
        inventario_antes = len(tienda_vendible.obtener_inventario())
        resultado = tienda_vendible.vender_por_nombre("Mesa Vendible", "Juan")
        assert "venta realizada exitosamente" in resultado.lower()
        inventario_despues = len(tienda_vendible.obtener_inventario())
        assert inventario_despues == inventario_antes - 1

    def test_vender_mueble_inexistente(self, tienda_vendible):
        resultado = tienda_vendible.vender_por_nombre("NoExiste")
        assert "error" in resultado.lower()

    def test_realizar_venta_retorna_diccionario_y_elimina_inventario(self, tienda_vendible):
        mueble = tienda_vendible.obtener_inventario()[0]
        inventario_antes = len(tienda_vendible.obtener_inventario())

        venta = tienda_vendible.realizar_venta(mueble, "Cliente Test")

        assert isinstance(venta, dict)
        assert "precio_final" in venta
        assert len(tienda_vendible.obtener_inventario()) == inventario_antes - 1

    def test_realizar_venta_mueble_fuera_de_inventario(self, tienda_vendible):
        mueble = Silla("No Disponible", "Tela", "Rojo", 80.0)
        resultado = tienda_vendible.realizar_venta(mueble, "Cliente")
        assert isinstance(resultado, dict)
        assert "error" in resultado


class TestTiendaComposicion:
    """Pruebas para comedor (composición)."""

    @pytest.fixture
    def tienda(self):
        return TiendaMuebles("Tienda Test")

    def test_agregar_comedor(self, tienda):
        mesa = Mesa("Mesa", "Madera", "Nogal", 400.0)
        silla = Silla("Silla", "Tela", "Gris", 100.0)
        comedor = Comedor("Comedor", mesa, [silla])

        resultado = tienda.agregar_comedor(comedor)
        assert "agregado exitosamente" in resultado.lower()
        assert len(tienda.obtener_comedores()) == 1

    def test_obtener_comedores_vacio(self, tienda):
        comedores = tienda.obtener_comedores()
        assert comedores == []

    def test_obtener_comedores_multiples(self, tienda):
        mesa1 = Mesa("Mesa 1", "Madera", "Nogal", 400.0)
        mesa2 = Mesa("Mesa 2", "Metal", "Plateado", 350.0)
        silla = Silla("Silla", "Tela", "Gris", 100.0)

        tienda.agregar_comedor(Comedor("Comedor 1", mesa1, [silla]))
        tienda.agregar_comedor(Comedor("Comedor 2", mesa2, [silla, silla]))

        assert len(tienda.obtener_comedores()) == 2


class TestTiendaCalculos:
    """Pruebas para cálculos de precio e inventario."""

    @pytest.fixture
    def tienda_con_precios(self):
        tienda = TiendaMuebles("Tienda Test")
        tienda.agregar_mueble(Mesa("Mesa", "Madera", "Nogal", 400.0, forma="rectangular"))
        tienda.agregar_mueble(Silla("Silla", "Tela", "Gris", 100.0))
        return tienda

    def test_calcular_valor_inventario(self, tienda_con_precios):
        valor = tienda_con_precios.calcular_valor_inventario()
        assert valor > 0
        assert isinstance(valor, float)

    def test_calcular_precio_final_con_descuento(self, tienda_con_precios):
        tienda_con_precios.aplicar_descuento("Sillas", 0.10)
        precio = tienda_con_precios.calcular_precio_final("Silla")
        assert precio is not None
        assert precio > 0

    def test_calcular_precio_final_inexistente(self, tienda_con_precios):
        precio = tienda_con_precios.calcular_precio_final("NoExiste")
        assert precio is None

    def test_contar_tipos_muebles_privado(self, tienda_con_precios):
        conteo = tienda_con_precios._contar_tipos_muebles()
        assert isinstance(conteo, dict)
        assert conteo.get("Mesa", 0) == 1
        assert conteo.get("Silla", 0) == 1


class TestTiendaReporte:
    """Pruebas para reportes."""

    @pytest.fixture
    def tienda_con_datos(self):
        tienda = TiendaMuebles("Tienda Test")
        tienda.agregar_mueble(Mesa("Mesa 1", "Madera", "Nogal", 400.0))
        tienda.agregar_mueble(Silla("Silla 1", "Tela", "Gris", 100.0))
        tienda.agregar_mueble(Silla("Silla 2", "Tela", "Azul", 120.0))
        tienda.aplicar_descuento("Sillas", 10)
        return tienda

    def test_generar_reporte_inventario(self, tienda_con_datos):
        reporte = tienda_con_datos.generar_reporte_inventario()
        assert isinstance(reporte, str)
        assert len(reporte) > 0
        assert "reporte de inventario" in reporte.lower()
        assert "descuentos activos" in reporte.lower()
