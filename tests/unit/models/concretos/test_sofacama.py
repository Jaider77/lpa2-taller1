"""
Pruebas unitarias para la clase SofaCama (herencia múltiple).
"""

from src.models.concretos.sofacama import SofaCama


class TestSofaCamaInstanciacion:
    """Pruebas para la instanciación de SofaCama."""

    def test_crear_sofacama_basica(self):
        """Prueba crear un sofá cama básico."""
        sofacama = SofaCama("Sofá Cama", "Tela", "Gris", 700.0)
        assert sofacama.nombre == "Sofá Cama"
        assert sofacama.precio_base == 700.0

    def test_crear_sofacama_completa(self):
        """Prueba crear sofá cama con todos los parámetros."""
        sofacama = SofaCama(
            "Sofá Cama Moderno",
            "Cuero",
            "Negro",
            1000.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            tamaño_colchon="Queen",
            es_reclinable=True,
            incluye_almacenamiento=True
        )
        assert sofacama.capacidad_personas == 3
        assert sofacama.tamaño_colchon == "Queen"


class TestSofaCamaHerenciaMultiple:
    """Pruebas para verificar la herencia múltiple."""

    def test_sofacama_combina_caracteristicas_sofa(self):
        """Prueba que SofaCama tiene características de Sofá."""
        sofacama = SofaCama("Sofá Cama", "Tela", "Gris", 700.0, capacidad_personas=3)
        assert sofacama.capacidad_personas == 3

    def test_sofacama_combina_caracteristicas_cama(self):
        """Prueba que SofaCama tiene características de Cama."""
        sofacama = SofaCama(
            "Sofá Cama",
            "Tela",
            "Gris",
            700.0,
            tamaño_colchon="Matrimonial"
        )
        assert sofacama.tamaño_colchon == "Matrimonial"

    def test_sofacama_calcula_precio_complejo(self):
        """Prueba que SofaCama calcula precio considerando ambas características."""
        sofacama = SofaCama(
            "Sofá Cama",
            "Cuero",
            "Negro",
            500.0,
            capacidad_personas=3,
            material_tapizado="Cuero",
            tamaño_colchon="Queen"
        )
        precio = sofacama.calcular_precio()
        # Debe ser más caro que un sofá o cama simple
        assert precio > 500.0


class TestSofaCamaObtenerDescripcion:
    """Pruebas para obtener descripción."""

    def test_obtener_descripcion(self):
        """Prueba obtener descripción de sofá cama."""
        sofacama = SofaCama(
            "Sofá Cama Moderno",
            "Tela",
            "Gris",
            800.0,
            tamaño_colchon="Queen"
        )
        descripcion = sofacama.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Sofá Cama" in descripcion or "sofá" in descripcion.lower()
