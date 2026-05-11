"""
Pruebas exhaustivas para la clase SofaCama.
"""

from src.models.concretos.sofacama import SofaCama


class TestSofaCamaBasico:
    """Pruebas básicas de instanciación."""

    def test_crear_sofacama_default(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        assert sofacama.nombre == "SofaCama"
        assert sofacama.material == "Tela"
        assert sofacama.color == "Gris"
        assert sofacama.precio_base == 1000.0
        assert sofacama.modo_actual == "sofa"

    def test_crear_sofacama_personalizado(self):
        sofacama = SofaCama(
            nombre="SofaCama Premium",
            material="Cuero",
            color="Negro",
            precio_base=1500.0,
            capacidad_personas=4,
            material_tapizado="Cuero",
            tamaño_cama="matrimonial",
            incluye_colchon=True,
            mecanismo_conversion="extensible",
        )
        assert sofacama.nombre == "SofaCama Premium"
        assert sofacama.capacidad_personas == 4
        assert sofacama.tamaño_cama == "matrimonial"
        assert sofacama.material_tapizado == "Cuero"


class TestSofaCamaPrecio:
    """Pruebas para cálculo de precio."""

    def test_calcular_precio_basico(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        precio = sofacama.calcular_precio()
        assert precio > 0
        assert isinstance(precio, (int, float))

    def test_calcular_precio_con_colchon_y_mecanismo(self):
        sofacama = SofaCama(
            "SofaCama",
            "Tela",
            "Gris",
            1000.0,
            incluye_colchon=True,
            mecanismo_conversion="hidraulico",
            tamaño_cama="queen",
        )
        precio = sofacama.calcular_precio()
        assert precio > 1000.0
        assert precio == round(precio, 2)

    def test_calcular_precio_varios_tamanos(self):
        sofacama_king = SofaCama(
            "SofaCama",
            "Tela",
            "Gris",
            1000.0,
            tamaño_cama="king",
            incluye_colchon=False,
        )
        sofacama_matrimonial = SofaCama(
            "SofaCama",
            "Tela",
            "Gris",
            1000.0,
            tamaño_cama="matrimonial",
            incluye_colchon=False,
        )
        assert sofacama_king.calcular_precio() > sofacama_matrimonial.calcular_precio()


class TestSofaCamaFuncionalidad:
    """Pruebas para funcionalidad del sofá-cama."""

    def test_sofacama_usa_modo_cama_y_sofa(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        assert sofacama.modo_actual == "sofa"

        mensaje = sofacama.convertir_a_cama()
        assert "convertido a cama" in mensaje.lower()
        assert sofacama.modo_actual == "cama"

        mensaje2 = sofacama.convertir_a_sofa()
        assert "convertida a sofá" in mensaje2.lower()
        assert sofacama.modo_actual == "sofa"

    def test_convertir_a_cama_dos_veces_retorna_mensaje(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        sofacama.convertir_a_cama()
        mensaje = sofacama.convertir_a_cama()
        assert "ya está en modo cama" in mensaje.lower()

    def test_convertir_a_sofa_dos_veces_retorna_mensaje(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        mensaje = sofacama.convertir_a_sofa()
        assert "ya está en modo sofá" in mensaje.lower()

    def test_obtener_descripcion_contiene_valores_clave(self):
        sofacama = SofaCama("SofaCama Premium", "Cuero", "Negro", 1500.0)
        descripcion = sofacama.obtener_descripcion()
        assert "Sofá-Cama" in descripcion
        assert "Precio final" in descripcion

    def test_obtener_capacidad_total_retorna_diccionario(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0, tamaño_cama="king")
        capacidades = sofacama.obtener_capacidad_total()
        assert capacidades["como_sofa"] == sofacama.capacidad_personas
        assert capacidades["como_cama"] == 2

    def test_str_muestra_modo_actual(self):
        sofacama = SofaCama("SofaCama", "Tela", "Gris", 1000.0)
        assert "modo: sofa" in str(sofacama).lower()
