"""
Pruebas unitarias para la clase TiendaMuebles (servicio).

Conceptos probados:
- Inicialización de la tienda
- Gestión de inventario (agregar/obtener muebles)
- Cálculo de estadísticas
- Búsquedas y filtros
- Descuentos
"""

import pytest
from src.services.tienda import TiendaMuebles
from src.models.concretos.silla import Silla
from src.models.concretos.mesa import Mesa
from src.models.concretos.cama import Cama
from src.models.composicion.comedor import Comedor


class TestTiendaMueblesInstanciacion:
    """Pruebas para la instanciación de TiendaMuebles."""

    def test_crear_tienda_default(self):
        """Prueba crear una tienda con nombre por defecto."""
        tienda = TiendaMuebles()
        assert tienda.nombre == "Mueblería OOP"

    def test_crear_tienda_con_nombre_personalizado(self):
        """Prueba crear una tienda con nombre personalizado."""
        tienda = TiendaMuebles(nombre_tienda="Muebles Premium")
        assert tienda.nombre == "Muebles Premium"

    def test_tienda_inicio_vacia(self):
        """Prueba que una tienda nueva está vacía."""
        tienda = TiendaMuebles()
        # Verificar que está vacía
        assert len(tienda.obtener_inventario()) == 0


class TestTiendaMueblesInventario:
    """Pruebas para la gestión del inventario."""
    
    @pytest.fixture
    def tienda_vacia(self):
        """Fixture que proporciona una tienda vacía."""
        return TiendaMuebles()
    
    @pytest.fixture
    def silla_muestra(self):
        """Fixture que proporciona una silla de muestra."""
        return Silla("Silla Prueba", "Madera", "Rojo", 50.0)
    
    @pytest.fixture
    def mesa_muestra(self):
        """Fixture que proporciona una mesa de muestra."""
        return Mesa("Mesa Prueba", "Madera", "Rojo", 100.0)

    def test_agregar_mueble_al_inventario(self, tienda_vacia, silla_muestra):
        """Prueba agregar un mueble al inventario."""
        resultado = tienda_vacia.agregar_mueble(silla_muestra)
        
        assert "exitosamente" in resultado.lower() or "agregado" in resultado.lower()
        assert len(tienda_vacia.obtener_inventario()) == 1

    def test_agregar_multiples_muebles(self, tienda_vacia, silla_muestra, mesa_muestra):
        """Prueba agregar múltiples muebles."""
        tienda_vacia.agregar_mueble(silla_muestra)
        tienda_vacia.agregar_mueble(mesa_muestra)
        
        assert len(tienda_vacia.obtener_inventario()) == 2

    def test_obtener_inventario(self, tienda_vacia, silla_muestra):
        """Prueba obtener el inventario."""
        tienda_vacia.agregar_mueble(silla_muestra)
        inventario = tienda_vacia.obtener_inventario()
        
        assert isinstance(inventario, list)
        assert silla_muestra in inventario

    def test_inventario_retorna_copia(self, tienda_vacia, silla_muestra):
        """Prueba que obtener_inventario retorna una copia."""
        tienda_vacia.agregar_mueble(silla_muestra)
        inventario = tienda_vacia.obtener_inventario()
        inventario_original_len = len(inventario)
        
        # Modificar la copia
        inventario.append("Mueble Falso")
        
        # El inventario original no debe cambiar
        assert len(tienda_vacia.obtener_inventario()) == inventario_original_len


class TestTiendaMueblesEstadisticas:
    """Pruebas para las estadísticas de la tienda."""
    
    @pytest.fixture
    def tienda_con_inventario(self):
        """Fixture que proporciona una tienda con inventario."""
        tienda = TiendaMuebles()
        tienda.agregar_mueble(Silla("Silla 1", "Madera", "Rojo", 50.0))
        tienda.agregar_mueble(Silla("Silla 2", "Madera", "Rojo", 50.0))
        tienda.agregar_mueble(Mesa("Mesa 1", "Madera", "Rojo", 100.0))
        return tienda

    def test_obtener_estadisticas(self, tienda_con_inventario):
        """Prueba obtener estadísticas de la tienda."""
        stats = tienda_con_inventario.obtener_estadisticas()
        
        assert isinstance(stats, dict)
        assert "total_muebles" in stats
        assert stats["total_muebles"] == 3

    def test_estadisticas_valor_inventario(self, tienda_con_inventario):
        """Prueba que las estadísticas incluyen el valor del inventario."""
        stats = tienda_con_inventario.obtener_estadisticas()
        
        assert "valor_inventario" in stats
        assert stats["valor_inventario"] > 0

    def test_estadisticas_tipos_muebles(self, tienda_con_inventario):
        """Prueba que las estadísticas incluyen tipos de muebles."""
        stats = tienda_con_inventario.obtener_estadisticas()
        
        assert "tipos_muebles" in stats
        assert "Silla" in stats["tipos_muebles"]
        assert "Mesa" in stats["tipos_muebles"]

    def test_estadisticas_tienda_vacia(self):
        """Prueba estadísticas de tienda vacía."""
        tienda = TiendaMuebles()
        stats = tienda.obtener_estadisticas()
        
        assert stats["total_muebles"] == 0
        assert stats["valor_inventario"] == 0


class TestTiendaMueblesDescuentos:
    """Pruebas para el sistema de descuentos."""
    
    @pytest.fixture
    def tienda_vacia(self):
        """Fixture que proporciona una tienda vacía."""
        return TiendaMuebles()

    def test_aplicar_descuento(self, tienda_vacia):
        """Prueba aplicar un descuento."""
        resultado = tienda_vacia.aplicar_descuento("Silla", 0.1)
        
        assert "exitosamente" in resultado.lower() or "aplicado" in resultado.lower()

    def test_descuento_se_registra(self, tienda_vacia):
        """Prueba que el descuento se registra."""
        tienda_vacia.aplicar_descuento("Silla", 0.1)
        stats = tienda_vacia.obtener_estadisticas()
        
        assert "descuentos_activos" in stats
        assert "Silla" in stats["descuentos_activos"]
        assert stats["descuentos_activos"]["Silla"] == 0.1

    def test_remover_descuento(self, tienda_vacia):
        """Prueba remover un descuento."""
        tienda_vacia.aplicar_descuento("Silla", 0.1)
        resultado = tienda_vacia.remover_descuento("Silla")
        
        assert "exitosamente" in resultado.lower() or "removido" in resultado.lower()
        
        stats = tienda_vacia.obtener_estadisticas()
        assert "Silla" not in stats["descuentos_activos"] or stats["descuentos_activos"]["Silla"] == 0


class TestTiendaMueblesVentas:
    """Pruebas para el registro de ventas."""
    
    @pytest.fixture
    def tienda_con_muebles(self):
        """Fixture que proporciona una tienda con muebles."""
        tienda = TiendaMuebles()
        tienda.agregar_mueble(Silla("Silla", "Madera", "Rojo", 50.0))
        tienda.agregar_mueble(Mesa("Mesa", "Madera", "Rojo", 100.0))
        return tienda

    def test_vender_mueble_existente(self, tienda_con_muebles):
        """Prueba vender un mueble existente."""
        resultado = tienda_con_muebles.vender_por_nombre("Silla")
        
        assert "exitosamente" in resultado.lower() or "vendido" in resultado.lower()
        assert len(tienda_con_muebles.obtener_inventario()) == 1

    def test_vender_mueble_inexistente(self, tienda_con_muebles):
        """Prueba vender un mueble que no existe."""
        resultado = tienda_con_muebles.vender_por_nombre("Mueble Inexistente")
        
        assert "Error" in resultado or "no" in resultado.lower()

    def test_registro_de_venta(self, tienda_con_muebles):
        """Prueba que se registra la venta."""
        tienda_con_muebles.vender_por_nombre("Silla")
        stats = tienda_con_muebles.obtener_estadisticas()
        
        assert stats["ventas_realizadas"] >= 1


class TestTiendaMueblesComposicion:
    """Pruebas para la gestión de comedores."""
    
    @pytest.fixture
    def tienda_vacia(self):
        """Fixture que proporciona una tienda vacía."""
        return TiendaMuebles()

    def test_agregar_comedor(self, tienda_vacia):
        """Prueba agregar un comedor."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        sillas = [Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(4)]
        comedor = Comedor("Comedor", mesa, sillas)
        
        resultado = tienda_vacia.agregar_comedor(comedor)
        
        assert "exitosamente" in resultado.lower() or "agregado" in resultado.lower()

    def test_obtener_comedores(self, tienda_vacia):
        """Prueba obtener comedores de la tienda."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa)
        tienda_vacia.agregar_comedor(comedor)
        
        comedores = tienda_vacia.obtener_comedores()
        assert len(comedores) == 1


class TestTiendaMueblesFiltroBusqueda:
    """Pruebas para filtrado y búsqueda."""
    
    @pytest.fixture
    def tienda_con_inventario_variado(self):
        """Fixture que proporciona una tienda con varios muebles."""
        tienda = TiendaMuebles()
        tienda.agregar_mueble(Silla("Silla Madera", "Madera", "Rojo", 50.0))
        tienda.agregar_mueble(Silla("Silla Metal", "Metal", "Negro", 75.0))
        tienda.agregar_mueble(Mesa("Mesa Madera", "Madera", "Marrón", 100.0))
        tienda.agregar_mueble(Mesa("Mesa Metal", "Metal", "Gris", 150.0))
        return tienda

    def test_filtrar_por_tipo(self, tienda_con_inventario_variado):
        """Prueba filtrar muebles por tipo."""
        sillas = tienda_con_inventario_variado.filtrar_por_tipo("Silla")
        
        assert len(sillas) == 2
        assert all("Silla" in type(m).__name__ for m in sillas)

    def test_filtrar_por_material(self, tienda_con_inventario_variado):
        """Prueba filtrar muebles por material."""
        muebles_madera = tienda_con_inventario_variado.filtrar_por_material("Madera")
        
        assert len(muebles_madera) >= 2
        assert all(m.material == "Madera" for m in muebles_madera)

    def test_buscar_por_nombre(self, tienda_con_inventario_variado):
        """Prueba buscar mueble por nombre."""
        resultado = tienda_con_inventario_variado.buscar_por_nombre("Silla Madera")
        
        assert resultado is not None
        assert resultado.nombre == "Silla Madera"

    def test_buscar_por_nombre_inexistente(self, tienda_con_inventario_variado):
        """Prueba buscar mueble con nombre que no existe."""
        resultado = tienda_con_inventario_variado.buscar_por_nombre("Mueble Inexistente")
        
        assert resultado is None


class TestTiendaMueblesPrecio:
    """Pruebas para cálculos de precio."""
    
    @pytest.fixture
    def tienda_con_muebles(self):
        """Fixture que proporciona una tienda con muebles."""
        tienda = TiendaMuebles()
        tienda.agregar_mueble(Silla("Silla", "Madera", "Rojo", 50.0))
        tienda.agregar_mueble(Mesa("Mesa", "Madera", "Rojo", 100.0))
        return tienda

    def test_precio_mueble_sin_descuento(self, tienda_con_muebles):
        """Prueba obtener precio de mueble sin descuento."""
        silla = tienda_con_muebles.buscar_por_nombre("Silla")
        precio = tienda_con_muebles.calcular_precio_final("Silla")
        
        assert precio == silla.calcular_precio()

    def test_precio_mueble_con_descuento(self, tienda_con_muebles):
        """Prueba obtener precio de mueble con descuento."""
        tienda_con_muebles.aplicar_descuento("Silla", 0.1)
        
        silla = tienda_con_muebles.buscar_por_nombre("Silla")
        precio_original = silla.calcular_precio()
        precio_con_descuento = tienda_con_muebles.calcular_precio_final("Silla")
        
        assert precio_con_descuento < precio_original
        assert precio_con_descuento == precio_original * 0.9
