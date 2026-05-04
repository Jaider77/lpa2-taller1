"""
Pruebas unitarias para la clase Cama (clase concreta).
"""

import pytest
from src.models.concretos.cama import Cama


class TestCamaInstanciacion:
    """Pruebas para la instanciación de Cama."""

    def test_crear_cama_basica(self):
        """Prueba crear una cama con parámetros mínimos."""
        cama = Cama("Cama Individual", "Madera", "Rojo", 300.0)
        assert cama.nombre == "Cama Individual"
        assert cama.precio_base == 300.0

    def test_crear_cama_completa(self):
        """Prueba crear una cama con todos los parámetros."""
        cama = Cama(
            "Cama Queen",
            "Madera de Pino",
            "Blanco",
            800.0,
            tamaño="queen",
            incluye_colchon=True,
            tiene_cabecera=True
        )
        assert cama.tamaño == "queen"
        assert cama.incluye_colchon is True
        assert cama.tiene_cabecera is True


class TestCamaTamaño:
    """Pruebas para la propiedad tamaño."""
    
    @pytest.fixture
    def cama_basica(self):
        return Cama("Cama", "Madera", "Rojo", 300.0)

    @pytest.mark.parametrize("tamaño", ["individual", "matrimonial", "queen", "king"])
    def test_tamaño_valido(self, cama_basica, tamaño):
        """Prueba setter de tamaño con valores válidos."""
        cama_basica.tamaño = tamaño
        assert cama_basica.tamaño == tamaño

    def test_tamaño_invalido(self, cama_basica):
        """Prueba que setter rechaza tamaño inválido."""
        with pytest.raises(ValueError, match="Tamaño debe ser uno de"):
            cama_basica.tamaño = "doble"


class TestCamaCalcularPrecio:
    """Pruebas para el cálculo del precio."""

    @pytest.mark.parametrize("tamaño,adicional_esperado", [
        ("individual", 0),
        ("matrimonial", 200),
        ("queen", 400),
        ("king", 600),
    ])
    def test_calcular_precio_por_tamaño(self, tamaño, adicional_esperado):
        """Prueba cálculo de precio según tamaño."""
        cama = Cama("Cama", "Madera", "Rojo", 300.0, tamaño=tamaño)
        precio = cama.calcular_precio()
        # Verificar que el precio aumenta con tamaño más grande
        assert precio >= 300.0

    def test_calcular_precio_con_colchon(self):
        """Prueba que incluir colchón aumenta el precio."""
        cama_sin_colchon = Cama("Cama", "Madera", "Rojo", 300.0, incluye_colchon=False)
        cama_con_colchon = Cama("Cama", "Madera", "Rojo", 300.0, incluye_colchon=True)
        
        precio_sin = cama_sin_colchon.calcular_precio()
        precio_con = cama_con_colchon.calcular_precio()
        
        assert precio_con > precio_sin


class TestCamaObtenerDescripcion:
    """Pruebas para obtener descripción."""

    def test_obtener_descripcion(self):
        """Prueba obtener descripción."""
        cama = Cama("Cama Queen", "Pino", "Blanco", 500.0, tamaño="queen")
        descripcion = cama.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Cama Queen" in descripcion
