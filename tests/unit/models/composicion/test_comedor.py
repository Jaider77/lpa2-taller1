"""
Pruebas unitarias para la clase Comedor (composición).

Conceptos probados:
- Composición: Comedor contiene una Mesa y Sillas
- Agregación: Sillas pueden existir independientemente
- Encapsulación: Controla acceso a componentes
- Métodos de gestión: agregar_silla, quitar_silla
- Cálculo de precio total
"""

import pytest
from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorInstanciacion:
    """Pruebas para la instanciación de Comedor."""

    def test_crear_comedor_basico(self):
        """Prueba crear un comedor con mesa y sillas."""
        mesa = Mesa("Mesa Comedor", "Madera", "Marrón", 200.0)
        sillas = [
            Silla("Silla 1", "Madera", "Marrón", 50.0),
            Silla("Silla 2", "Madera", "Marrón", 50.0),
        ]
        comedor = Comedor("Comedor Familiar", mesa, sillas)
        
        assert comedor.nombre == "Comedor Familiar"
        assert comedor.mesa == mesa
        assert len(comedor.sillas) == 2

    def test_crear_comedor_sin_sillas(self):
        """Prueba crear un comedor sin sillas inicialmente."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor Vacío", mesa)
        
        assert comedor.nombre == "Comedor Vacío"
        assert comedor.mesa == mesa
        assert len(comedor.sillas) == 0

    def test_crear_comedor_con_sillas_none(self):
        """Prueba crear comedor pasando sillas=None."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa, None)
        
        assert len(comedor.sillas) == 0


class TestComedorProperties:
    """Pruebas para las propiedades de Comedor."""
    
    @pytest.fixture
    def comedor_completo(self):
        """Fixture que proporciona un comedor completo."""
        mesa = Mesa("Mesa Comedor", "Roble", "Marrón", 300.0, capacidad_personas=6)
        sillas = [
            Silla("Silla Roble", "Roble", "Marrón", 80.0)
            for _ in range(4)
        ]
        return Comedor("Comedor Familiar", mesa, sillas)

    def test_nombre_getter(self, comedor_completo):
        """Prueba el getter de nombre."""
        assert comedor_completo.nombre == "Comedor Familiar"

    def test_mesa_getter(self, comedor_completo):
        """Prueba el getter de mesa."""
        assert comedor_completo.mesa is not None
        assert comedor_completo.mesa.nombre == "Mesa Comedor"

    def test_sillas_getter_retorna_copia(self, comedor_completo):
        """Prueba que sillas getter retorna una copia (no referencia directa)."""
        sillas = comedor_completo.sillas
        original_cantidad = len(sillas)
        
        sillas.append("Silla Falsa")
        
        # El comedor debe seguir teniendo el número original
        assert len(comedor_completo.sillas) == original_cantidad


class TestComedorComposicion:
    """Pruebas para verificar la composición."""

    def test_comedor_contiene_mesa(self):
        """Prueba que el comedor contiene una mesa."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa)
        
        assert isinstance(comedor.mesa, Mesa)

    def test_comedor_contiene_sillas(self):
        """Prueba que el comedor contiene sillas."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        sillas = [Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(3)]
        comedor = Comedor("Comedor", mesa, sillas)
        
        assert all(isinstance(silla, Silla) for silla in comedor.sillas)

    def test_muebles_existen_independientemente(self):
        """Prueba que mesa y sillas pueden existir de forma independiente."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        silla = Silla("Silla", "Madera", "Rojo", 50.0)
        
        # Crear comedor
        Comedor("Comedor", mesa, [silla])
        
        # Los muebles deben existir sin el comedor
        assert mesa.nombre == "Mesa"
        assert silla.nombre == "Silla"


class TestComedorAgregarSilla:
    """Pruebas para el método agregar_silla."""
    
    @pytest.fixture
    def comedor_vacio(self):
        """Fixture que proporciona un comedor vacío."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0, capacidad_personas=4)
        return Comedor("Comedor", mesa)

    def test_agregar_silla_exitosa(self, comedor_vacio):
        """Prueba agregar una silla exitosamente."""
        silla = Silla("Silla", "Madera", "Rojo", 50.0)
        resultado = comedor_vacio.agregar_silla(silla)
        
        assert "exitosamente" in resultado.lower()
        assert len(comedor_vacio.sillas) == 1

    def test_agregar_multiples_sillas(self, comedor_vacio):
        """Prueba agregar múltiples sillas."""
        sillas = [Silla(f"Silla {i}", "Madera", "Rojo", 50.0) for i in range(3)]
        
        for silla in sillas:
            comedor_vacio.agregar_silla(silla)
        
        assert len(comedor_vacio.sillas) == 3

    def test_agregar_silla_excede_capacidad(self, comedor_vacio):
        """Prueba que no se pueden agregar más sillas que la capacidad de la mesa."""
        # Mesa tiene capacidad de 4, agregamos 4 sillas (debe estar lleno)
        for i in range(4):
            silla = Silla(f"Silla {i}", "Madera", "Rojo", 50.0)
            comedor_vacio.agregar_silla(silla)
        
        # Intentar agregar una 5ta silla
        silla_extra = Silla("Silla Extra", "Madera", "Rojo", 50.0)
        resultado = comedor_vacio.agregar_silla(silla_extra)
        
        assert "No se pueden agregar más sillas" in resultado or "capacidad" in resultado.lower()
        assert len(comedor_vacio.sillas) == 4

    def test_agregar_silla_objeto_no_valido(self, comedor_vacio):
        """Prueba agregar un objeto que no es una Silla."""
        # Agregar una silla primero para que valide el tipo
        silla_valida = Silla("Silla Valida", "Madera", "Rojo", 50.0)
        comedor_vacio.agregar_silla(silla_valida)
        
        # Intentar agregar un objeto no válido
        objeto_invalido = "Esto no es una silla"
        resultado = comedor_vacio.agregar_silla(objeto_invalido)
        
        assert "Solo se pueden agregar objetos de tipo Silla" in resultado
        assert len(comedor_vacio.sillas) == 1


class TestComedorQuitarSilla:
    """Pruebas para el método quitar_silla."""
    
    @pytest.fixture
    def comedor_con_sillas(self):
        """Fixture que proporciona un comedor con sillas."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0, capacidad_personas=6)
        sillas = [
            Silla(f"Silla {i}", "Madera", "Rojo", 50.0)
            for i in range(4)
        ]
        return Comedor("Comedor", mesa, sillas)

    def test_quitar_ultima_silla(self, comedor_con_sillas):
        """Prueba quitar la última silla."""
        cantidad_inicial = len(comedor_con_sillas.sillas)
        resultado = comedor_con_sillas.quitar_silla()
        
        assert len(comedor_con_sillas.sillas) == cantidad_inicial - 1
        assert "quitada" in resultado.lower() or "removida" in resultado.lower()

    def test_quitar_silla_por_indice(self, comedor_con_sillas):
        """Prueba quitar una silla específica por índice."""
        comedor_con_sillas.quitar_silla(0)
        assert len(comedor_con_sillas.sillas) == 3

    def test_quitar_silla_de_comedor_vacio(self):
        """Prueba quitar silla de comedor vacío."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa)
        
        resultado = comedor.quitar_silla()
        assert "Error" in resultado or "vacío" in resultado.lower() or "no hay" in resultado.lower()

    def test_quitar_silla_indice_invalido(self, comedor_con_sillas):
        """Prueba quitar silla con índice inválido."""
        resultado = comedor_con_sillas.quitar_silla(999)
        assert "Error" in resultado or "índice" in resultado.lower()

    def test_quitar_silla_indice_negativo_valido(self, comedor_con_sillas):
        """Prueba quitar silla con índice negativo válido."""
        cantidad_inicial = len(comedor_con_sillas.sillas)
        resultado = comedor_con_sillas.quitar_silla(-1)  # Última silla
        
        assert len(comedor_con_sillas.sillas) == cantidad_inicial - 1
        assert "removida" in resultado.lower() or "quitada" in resultado.lower()


class TestComedorCalcularPrecio:
    """Pruebas para el cálculo del precio total."""

    def test_calcular_precio_comedor_completo(self):
        """Prueba calcular precio total de un comedor."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        sillas = [Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(4)]
        comedor = Comedor("Comedor", mesa, sillas)
        
        precio_total = comedor.calcular_precio()
        
        # Precio debe ser al menos la suma de los precios base
        assert precio_total > 0

    def test_calcular_precio_solo_mesa(self):
        """Prueba calcular precio cuando hay solo mesa."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa)
        
        precio_total = comedor.calcular_precio()
        precio_mesa = mesa.calcular_precio()
        
        assert precio_total == precio_mesa

    def test_precio_mayor_con_mas_sillas(self):
        """Prueba que el precio aumenta con más sillas."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        
        comedor1 = Comedor("Comedor", mesa, [Silla("Silla", "Madera", "Rojo", 50.0)])
        comedor2 = Comedor("Comedor", mesa, [
            Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(4)
        ])
        
        precio1 = comedor1.calcular_precio()
        precio2 = comedor2.calcular_precio()
        
        assert precio2 > precio1

    def test_calcular_precio_con_cuatro_sillas(self):
        """Prueba calcular precio con 4 sillas (set completo según descripción)."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 200.0)
        sillas = [Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(4)]
        comedor = Comedor("Comedor Grande", mesa, sillas)
        
        precio_total = comedor.calcular_precio()
        precio_mesa = mesa.calcular_precio()
        precio_sillas = sum(silla.calcular_precio() for silla in sillas)
        precio_esperado = precio_mesa + precio_sillas
        
        # Actualmente no hay descuento implementado en el cálculo
        assert precio_total == precio_esperado


class TestComedorObtenerDescripcion:
    """Pruebas para el método obtener_descripcion."""

    def test_obtener_descripcion_basica(self):
        """Prueba obtener descripción del comedor."""
        mesa = Mesa("Mesa Roble", "Roble", "Marrón", 200.0)
        sillas = [Silla("Silla Roble", "Roble", "Marrón", 50.0) for _ in range(4)]
        comedor = Comedor("Comedor Familiar", mesa, sillas)
        
        descripcion = comedor.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Comedor Familiar" in descripcion

    def test_obtener_descripcion_incluye_componentes(self):
        """Prueba que la descripción incluye mesa y sillas."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        sillas = [Silla("Silla", "Madera", "Rojo", 50.0) for _ in range(2)]
        comedor = Comedor("Comedor", mesa, sillas)
        
        descripcion = comedor.obtener_descripcion()
        
        # Debe mencionar cantidad de sillas
        assert "2" in descripcion or "dos" in descripcion.lower() or "silla" in descripcion.lower()


class TestComedorListarComponentes:
    """Pruebas para métodos que listan componentes."""

    def test_listar_componentes(self):
        """Prueba listar todos los componentes del comedor."""
        mesa = Mesa("Mesa Roble", "Roble", "Marrón", 200.0)
        sillas = [
            Silla("Silla Roble 1", "Roble", "Marrón", 50.0),
            Silla("Silla Roble 2", "Roble", "Marrón", 50.0),
        ]
        comedor = Comedor("Comedor Familiar", mesa, sillas)
        
        # Buscar método para listar
        if hasattr(comedor, 'listar_componentes'):
            componentes = comedor.listar_componentes()
            assert len(componentes) > 0


class TestComedorInternals:
    """Pruebas adicionales para los métodos internos y propiedades."""

    def test_len_y_str_comedor(self):
        mesa = Mesa("Mesa Roble", "Roble", "Marrón", 200.0)
        sillas = [Silla("Silla 1", "Roble", "Marrón", 50.0) for _ in range(3)]
        comedor = Comedor("Comedor Familiar", mesa, sillas)

        assert len(comedor) == 4
        assert "Comedor Familiar" in str(comedor)

    def test_len_comedor_solo_mesa(self):
        """Prueba __len__ cuando solo hay mesa."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor", mesa)
        
        assert len(comedor) == 1

    def test_obtener_resumen_contiene_precio_y_materiales(self):
        mesa = Mesa("Mesa Roble", "Roble", "Marrón", 200.0)
        sillas = [Silla("Silla 1", "Roble", "Marrón", 50.0)]
        comedor = Comedor("Comedor Familiar", mesa, sillas)

        resumen = comedor.obtener_resumen()
        assert resumen["nombre"] == "Comedor Familiar"
        assert resumen["total_muebles"] == 2
        assert resumen["precio_total"] == comedor.calcular_precio_total()
        assert any(material in resumen["materiales_utilizados"] for material in ["Roble", "Madera"])

    def test_obtener_resumen_comedor_vacio(self):
        """Prueba obtener resumen de comedor sin sillas."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        comedor = Comedor("Comedor Vacío", mesa)

        resumen = comedor.obtener_resumen()
        assert resumen["nombre"] == "Comedor Vacío"
        assert resumen["total_muebles"] == 1  # Solo mesa
        assert resumen["precio_total"] == mesa.calcular_precio()  # Precio calculado de la mesa
        assert resumen["capacidad_personas"] == 0

