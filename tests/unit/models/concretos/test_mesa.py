"""
Pruebas unitarias para la clase Mesa (clase concreta).

Conceptos probados:
- Verificar que Mesa se instancia correctamente
- Herencia: que hereda propiedades de Superficie y Mueble
- Propiedades específicas: forma, capacidad_personas
- Cálculo de precio
- Validación de forma válida
"""

import pytest
from src.models.concretos.mesa import Mesa


class TestMesaInstanciacion:
    """Pruebas para la instanciación de Mesa."""

    def test_crear_mesa_basica(self):
        """Prueba crear una mesa con parámetros mínimos."""
        mesa = Mesa(
            nombre="Mesa Comedor",
            material="Madera",
            color="Rojo",
            precio_base=200.0
        )
        
        assert mesa.nombre == "Mesa Comedor"
        assert mesa.material == "Madera"
        assert mesa.color == "Rojo"
        assert mesa.precio_base == 200.0

    def test_crear_mesa_completa(self):
        """Prueba crear una mesa con todos los parámetros."""
        mesa = Mesa(
            nombre="Mesa Ejecutiva",
            material="Caoba",
            color="Marrón",
            precio_base=500.0,
            forma="rectangular",
            largo=180.0,
            ancho=90.0,
            altura=75.0,
            capacidad_personas=6
        )
        
        assert mesa.nombre == "Mesa Ejecutiva"
        assert mesa.forma == "rectangular"
        assert mesa.capacidad_personas == 6
        assert mesa.largo == 180.0
        assert mesa.ancho == 90.0
        assert mesa.altura == 75.0

    def test_mesa_valores_por_defecto(self):
        """Prueba que Mesa tiene valores por defecto correctos."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        
        assert mesa.forma == "rectangular"
        assert mesa.largo == 120.0
        assert mesa.ancho == 80.0
        assert mesa.altura == 75.0
        assert mesa.capacidad_personas == 4


class TestMesaForma:
    """Pruebas para la propiedad forma de Mesa."""
    
    @pytest.fixture
    def mesa_basica(self):
        """Fixture que proporciona una mesa básica."""
        return Mesa("Mesa", "Madera", "Rojo", 100.0)

    def test_forma_getter(self, mesa_basica):
        """Prueba el getter de forma."""
        assert mesa_basica.forma == "rectangular"

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_forma_setter_valida(self, mesa_basica, forma):
        """Prueba el setter de forma con valores válidos."""
        mesa_basica.forma = forma
        assert mesa_basica.forma == forma

    def test_forma_setter_invalida(self, mesa_basica):
        """Prueba que setter de forma rechaza valores inválidos."""
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa_basica.forma = "triangular"

    def test_forma_setter_vacia(self, mesa_basica):
        """Prueba que setter de forma rechaza valores vacíos."""
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa_basica.forma = ""


class TestMesaCapacidad:
    """Pruebas para la propiedad capacidad_personas de Mesa."""
    
    @pytest.fixture
    def mesa_basica(self):
        """Fixture que proporciona una mesa básica."""
        return Mesa("Mesa", "Madera", "Rojo", 100.0)

    def test_capacidad_getter(self, mesa_basica):
        """Prueba el getter de capacidad_personas."""
        assert mesa_basica.capacidad_personas == 4

    def test_capacidad_setter_valida(self, mesa_basica):
        """Prueba el setter de capacidad_personas con valor válido."""
        mesa_basica.capacidad_personas = 8
        assert mesa_basica.capacidad_personas == 8

    def test_capacidad_setter_cero(self, mesa_basica):
        """Prueba que capacidad_personas no puede ser 0."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            mesa_basica.capacidad_personas = 0

    def test_capacidad_setter_negativa(self, mesa_basica):
        """Prueba que capacidad_personas no puede ser negativa."""
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            mesa_basica.capacidad_personas = -2


class TestMesaDimensiones:
    """Pruebas para las dimensiones de Mesa (heredadas de Superficie)."""
    
    @pytest.fixture
    def mesa_basica(self):
        """Fixture que proporciona una mesa básica."""
        return Mesa("Mesa", "Madera", "Rojo", 100.0, largo=150.0, ancho=75.0, altura=80.0)

    def test_largo_getter(self, mesa_basica):
        """Prueba el getter de largo."""
        assert mesa_basica.largo == 150.0

    def test_largo_setter_valido(self, mesa_basica):
        """Prueba el setter de largo con valor válido."""
        mesa_basica.largo = 200.0
        assert mesa_basica.largo == 200.0

    def test_largo_setter_invalido(self, mesa_basica):
        """Prueba que setter de largo rechaza valores no positivos."""
        with pytest.raises(ValueError, match="El largo debe ser mayor a 0"):
            mesa_basica.largo = 0

    def test_ancho_getter(self, mesa_basica):
        """Prueba el getter de ancho."""
        assert mesa_basica.ancho == 75.0

    def test_ancho_setter_valido(self, mesa_basica):
        """Prueba el setter de ancho con valor válido."""
        mesa_basica.ancho = 100.0
        assert mesa_basica.ancho == 100.0

    def test_altura_getter(self, mesa_basica):
        """Prueba el getter de altura."""
        assert mesa_basica.altura == 80.0

    def test_altura_setter_valido(self, mesa_basica):
        """Prueba el setter de altura con valor válido."""
        mesa_basica.altura = 85.0
        assert mesa_basica.altura == 85.0


class TestMesaCalcularPrecio:
    """Pruebas para el cálculo del precio de Mesa."""

    @pytest.mark.parametrize("forma,capacidad,precio_base", [
        ("rectangular", 4, 100.0),
        ("redonda", 6, 150.0),
        ("cuadrada", 4, 120.0),
        ("ovalada", 8, 200.0),
    ])
    def test_calcular_precio_diferentes_formas(self, forma, capacidad, precio_base):
        """Prueba cálculo de precio con diferentes formas y capacidades."""
        mesa = Mesa(
            "Mesa",
            "Madera",
            "Rojo",
            precio_base,
            forma=forma,
            capacidad_personas=capacidad
        )
        precio = mesa.calcular_precio()
        
        # Verificar que el precio se calcula (no es exacto sin ver la implementación)
        assert precio > 0
        assert isinstance(precio, float)

    def test_calcular_precio_area_influye(self):
        """Prueba que el área influye en el precio."""
        mesa_pequena = Mesa("Mesa Pequeña", "Madera", "Rojo", 100.0, largo=100.0, ancho=60.0)
        mesa_grande = Mesa("Mesa Grande", "Madera", "Rojo", 100.0, largo=200.0, ancho=120.0)
        
        precio_pequena = mesa_pequena.calcular_precio()
        precio_grande = mesa_grande.calcular_precio()
        
        # Mesa más grande debe costar más
        assert precio_grande > precio_pequena


class TestMesaObtenerDescripcion:
    """Pruebas para el método obtener_descripcion de Mesa."""

    def test_obtener_descripcion_basica(self):
        """Prueba la descripción de una mesa básica."""
        mesa = Mesa("Mesa Comedor", "Roble", "Marrón", 200.0)
        descripcion = mesa.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Mesa Comedor" in descripcion
        assert "Roble" in descripcion

    def test_obtener_descripcion_incluye_dimensiones(self):
        """Prueba que la descripción incluye dimensiones."""
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0, largo=150.0, ancho=80.0)
        descripcion = mesa.obtener_descripcion()
        
        # Debe incluir información de dimensiones o forma
        assert len(descripcion) > 0
        assert ("rectangular" in descripcion.lower() or 
                "150" in descripcion or "80" in descripcion)


class TestMesaHerencia:
    """Pruebas para verificar la herencia correcta."""

    def test_hereda_de_superficie(self):
        """Prueba que Mesa hereda de Superficie."""
        from src.models.categorias.superficies import Superficie
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        assert isinstance(mesa, Superficie)

    def test_hereda_de_mueble(self):
        """Prueba que Mesa hereda de Mueble a través de Superficie."""
        from src.models.mueble import Mueble
        mesa = Mesa("Mesa", "Madera", "Rojo", 100.0)
        assert isinstance(mesa, Mueble)
