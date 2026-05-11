"""
Pruebas exhaustivas para la clase Cajonera.
"""

from src.models.concretos.cajonera import Cajonera


class TestCajoneraInstanciacion:
    """Pruebas de instanciación de Cajonera."""

    def test_instanciacion_basica(self):
        """Prueba instanciación con parámetros básicos."""
        cajonera = Cajonera("Cajonera Básica", "Madera", "Nogal", 150)
        assert cajonera.nombre == "Cajonera Básica"
        assert cajonera.material == "Madera"
        assert cajonera.color == "Nogal"
        assert cajonera.precio_base == 150
        assert cajonera.num_cajones == 3  # default
        assert not cajonera.tiene_ruedas  # default

    def test_instanciacion_completa(self):
        """Prueba instanciación con todos los parámetros."""
        cajonera = Cajonera("Cajonera Premium", "Metal", "Negro", 200, 5, True)
        assert cajonera.nombre == "Cajonera Premium"
        assert cajonera.material == "Metal"
        assert cajonera.color == "Negro"
        assert cajonera.precio_base == 200
        assert cajonera.num_cajones == 5
        assert cajonera.tiene_ruedas

    def test_instanciacion_sin_ruedas(self):
        """Prueba instanciación sin ruedas."""
        cajonera = Cajonera("Cajonera Simple", "Plástico", "Blanco", 100, 2, False)
        assert cajonera.num_cajones == 2
        assert not cajonera.tiene_ruedas


class TestCajoneraPrecio:
    """Pruebas de cálculo de precio."""

    def test_calcular_precio_basico(self):
        """Prueba precio con valores por defecto."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 100)
        # precio_base + num_cajones * 20 + (0 si no tiene ruedas)
        expected = 100 + 3 * 20  # 100 + 60 = 160
        assert cajonera.calcular_precio() == expected

    def test_calcular_precio_con_ruedas(self):
        """Prueba precio con ruedas."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 100, 3, True)
        # precio_base + num_cajones * 20 + 30 (ruedas)
        expected = 100 + 3 * 20 + 30  # 100 + 60 + 30 = 190
        assert cajonera.calcular_precio() == expected

    def test_calcular_precio_multiples_cajones(self):
        """Prueba precio con múltiples cajones."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 100, 5, False)
        # precio_base + 5 * 20
        expected = 100 + 100  # 200
        assert cajonera.calcular_precio() == expected

    def test_calcular_precio_multiples_cajones_con_ruedas(self):
        """Prueba precio con múltiples cajones y ruedas."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 100, 4, True)
        # precio_base + 4 * 20 + 30
        expected = 100 + 80 + 30  # 210
        assert cajonera.calcular_precio() == expected

    def test_calcular_precio_redondeo(self):
        """Prueba que el precio se redondea correctamente."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 105, 3, True)
        # 105 + 60 + 30 = 195, redondeo no cambia
        expected = 195
        assert cajonera.calcular_precio() == expected


class TestCajoneraDescripcion:
    """Pruebas de descripción."""

    def test_obtener_descripcion_basica(self):
        """Prueba descripción con valores por defecto."""
        cajonera = Cajonera("Cajonera Básica", "Madera", "Nogal", 150)
        descripcion = cajonera.obtener_descripcion()
        expected = ("Cajonera 'Cajonera Básica': Material=Madera, Color=Nogal, "
                   "Cajones=3, Ruedas=No, Precio base=$150")
        assert descripcion == expected

    def test_obtener_descripcion_con_ruedas(self):
        """Prueba descripción con ruedas."""
        cajonera = Cajonera("Cajonera Premium", "Metal", "Negro", 200, 5, True)
        descripcion = cajonera.obtener_descripcion()
        expected = ("Cajonera 'Cajonera Premium': Material=Metal, Color=Negro, "
                   "Cajones=5, Ruedas=Sí, Precio base=$200")
        assert descripcion == expected

    def test_obtener_descripcion_sin_ruedas(self):
        """Prueba descripción sin ruedas."""
        cajonera = Cajonera("Cajonera Simple", "Plástico", "Blanco", 100, 2, False)
        descripcion = cajonera.obtener_descripcion()
        expected = ("Cajonera 'Cajonera Simple': Material=Plástico, Color=Blanco, "
                   "Cajones=2, Ruedas=No, Precio base=$100")
        assert descripcion == expected


class TestCajoneraHerencia:
    """Pruebas de herencia de Mueble."""

    def test_herencia_mueble(self):
        """Prueba que Cajonera hereda de Mueble."""
        from src.models.mueble import Mueble
        assert issubclass(Cajonera, Mueble)

    def test_tiene_metodos_mueble(self):
        """Prueba que tiene métodos de Mueble."""
        cajonera = Cajonera("Test", "Madera", "Nogal", 100)
        assert hasattr(cajonera, "calcular_precio")
        assert hasattr(cajonera, "obtener_descripcion")
        assert hasattr(cajonera, "__str__")
        assert hasattr(cajonera, "__repr__")

    def test_str_method(self):
        """Prueba método __str__."""
        cajonera = Cajonera("Mi Cajonera", "Madera", "Nogal", 150)
        expected = "Mi Cajonera de Madera en color Nogal"
        assert str(cajonera) == expected

    def test_repr_method(self):
        """Prueba método __repr__."""
        cajonera = Cajonera("Mi Cajonera", "Madera", "Nogal", 150)
        expected = "Mueble(nombre='Mi Cajonera', material='Madera', color='Nogal', precio_base=150)"
        assert repr(cajonera) == expected
