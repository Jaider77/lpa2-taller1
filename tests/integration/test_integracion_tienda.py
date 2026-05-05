"""
Pruebas de integración básicas para el proyecto.

Estas pruebas verifican la integración entre múltiples componentes
del sistema.
"""

import pytest  # noqa: F401
from src.services.tienda import TiendaMuebles
from src.models.concretos.silla import Silla
from src.models.concretos.mesa import Mesa
from src.models.concretos.cama import Cama
from src.models.composicion.comedor import Comedor


class TestIntegracionTiendaCompleta:
    """Pruebas de integración de la tienda completa."""

    def test_crear_tienda_y_agregar_inventario(self):
        """Prueba crear una tienda y agregar muebles."""
        tienda = TiendaMuebles("Tienda Test")
        
        silla = Silla("Silla", "Madera", "Rojo", 50.0)
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        cama = Cama("Cama", "Madera", "Rojo", 200.0)
        
        tienda.agregar_mueble(silla)
        tienda.agregar_mueble(mesa)
        tienda.agregar_mueble(cama)
        
        assert len(tienda.obtener_inventario()) == 3

    def test_estadisticas_con_varios_muebles(self):
        """Prueba obtener estadísticas con inventario variado."""
        tienda = TiendaMuebles()
        
        for i in range(3):
            tienda.agregar_mueble(Silla(f"Silla {i}", "Madera", "Rojo", 50.0))
        
        for i in range(2):
            tienda.agregar_mueble(Mesa(f"Mesa {i}", "Madera", "Rojo", 100.0))
        
        stats = tienda.obtener_estadisticas()
        
        assert stats["total_muebles"] == 5
        assert "Silla" in stats["tipos_muebles"]
        assert "Mesa" in stats["tipos_muebles"]

    def test_comedor_completo_en_tienda(self):
        """Prueba crear un comedor y agregarlo a la tienda."""
        tienda = TiendaMuebles()
        
        mesa = Mesa("Mesa Comedor", "Roble", "Marrón", 300.0)
        sillas = [
            Silla("Silla Comedor", "Roble", "Marrón", 80.0)
            for _ in range(4)
        ]
        comedor = Comedor("Comedor Familiar", mesa, sillas)
        
        tienda.agregar_comedor(comedor)
        
        assert len(tienda.obtener_comedores()) == 1

    def test_flujo_venta_completo(self):
        """Prueba un flujo completo de venta."""
        tienda = TiendaMuebles()
        
        # Agregar muebles
        tienda.agregar_mueble(Silla("Silla Premium", "Cuero", "Negro", 150.0))
        
        # Verificar que está en inventario
        assert len(tienda.obtener_inventario()) == 1
        
        # Vender
        tienda.vender_por_nombre("Silla Premium")
        
        # Verificar que se vendió
        assert len(tienda.obtener_inventario()) == 0

    def test_aplicar_descuento_y_vender(self):
        """Prueba aplicar descuento y luego vender."""
        tienda = TiendaMuebles()
        
        tienda.agregar_mueble(Silla("Silla", "Madera", "Rojo", 100.0))
        tienda.aplicar_descuento("Silla", 0.2)
        
        # Obtener precio con descuento
        precio_con_descuento = tienda.calcular_precio_final("Silla")
        
        # Precio original * 0.8 = 80
        assert precio_con_descuento == 80.0

    def test_buscar_y_filtrar(self):
        """Prueba funcionalidad de búsqueda y filtrado."""
        tienda = TiendaMuebles()
        
        tienda.agregar_mueble(Silla("Silla Oak", "Roble", "Marrón", 60.0))
        tienda.agregar_mueble(Silla("Silla Pine", "Pino", "Blanco", 40.0))
        tienda.agregar_mueble(Mesa("Mesa Oak", "Roble", "Marrón", 150.0))
        
        # Buscar por nombre
        silla_oak = tienda.buscar_por_nombre("Silla Oak")
        assert silla_oak is not None
        assert silla_oak.material == "Roble"
        
        # Filtrar por material
        muebles_roble = tienda.filtrar_por_material("Roble")
        assert len(muebles_roble) == 2


class TestIntegracionPreciosComplejos:
    """Pruebas de integración para cálculos complejos de precios."""

    def test_precio_mueble_con_caracteristicas_multiples(self):
        """Prueba precio de mueble con múltiples características."""
        silla = Silla(
            "Silla Gamer Elite",
            "Cuero",
            "Negro",
            300.0,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            altura_regulable=True,
            tiene_ruedas=True
        )
        
        precio = silla.calcular_precio()
        
        # Debe ser significativamente más caro que el precio base
        assert precio > 300.0

    def test_precio_comedor_completo(self):
        """Prueba cálculo de precio de un comedor completo."""
        mesa = Mesa("Mesa", "Roble", "Marrón", 300.0, capacidad_personas=6)
        sillas = [
            Silla("Silla", "Roble", "Marrón", 80.0, tiene_respaldo=True, material_tapizado="Tela")
            for _ in range(6)
        ]
        comedor = Comedor("Comedor Familiar", mesa, sillas)
        
        precio_total = comedor.calcular_precio()
        
        # Debe ser suma de mesa + sillas
        precio_mesa = mesa.calcular_precio()
        precio_sillas = sum(s.calcular_precio() for s in sillas)
        
        assert precio_total == (precio_mesa + precio_sillas)


class TestIntegracionValidaciones:
    """Pruebas de integración para validaciones."""

    def test_no_se_puede_vender_mueble_inexistente(self):
        """Prueba que no se puede vender mueble que no existe."""
        tienda = TiendaMuebles()
        
        resultado = tienda.vender_por_nombre("Mueble Fantasma")
        
        assert "Error" in resultado or "no" in resultado.lower()

    def test_descuento_invalido_no_se_aplica(self):
        """Prueba que descuentos inválidos son rechazados."""
        tienda = TiendaMuebles()
        tienda.agregar_mueble(Silla("Silla", "Madera", "Rojo", 50.0))
        
        # Intentar aplicar descuento inválido
        resultado = tienda.aplicar_descuento("Silla", 1.5)  # noqa: F841
        
        # Dependiendo de la implementación, puede ser rechazado
        # o limitado a valores válidos
        stats = tienda.obtener_estadisticas()
        
        # Verificar que el descuento no es mayor a 1.0
        if "Silla" in stats["descuentos_activos"]:
            assert stats["descuentos_activos"]["Silla"] <= 1.0
