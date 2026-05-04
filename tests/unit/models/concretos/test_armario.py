"""
Pruebas unitarias para la clase Armario (clase concreta).

Nota: Armario NO hereda de Mueble en su implementación actual,
por lo que las pruebas se adaptan a su estructura.
"""

import pytest
from src.models.concretos.armario import Armario


class TestArmarioInstanciacion:
    """Pruebas para la instanciación de Armario."""

    def test_crear_armario_basico(self):
        """Prueba crear un armario con parámetros mínimos."""
        armario = Armario("Armario Básico", "MDF", "Blanco", 300)
        assert armario.nombre == "Armario Básico"
        assert armario.precio_base == 300

    def test_crear_armario_completo(self):
        """Prueba crear un armario con todos los parámetros."""
        armario = Armario(
            "Armario Grande",
            "Madera",
            "Nogal",
            600,
            num_puertas=4,
            num_cajones=6,
            tiene_espejos=True
        )
        assert armario.num_puertas == 4
        assert armario.num_cajones == 6
        assert armario.tiene_espejos is True

    def test_armario_valores_por_defecto(self):
        """Prueba valores por defecto de Armario."""
        armario = Armario("Armario", "MDF", "Blanco", 200)
        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False


class TestArmarioProperties:
    """Pruebas para las propiedades de Armario."""
    
    @pytest.fixture
    def armario_basico(self):
        return Armario("Armario", "MDF", "Blanco", 300)

    def test_nombre_property(self, armario_basico):
        """Prueba acceder al nombre."""
        assert armario_basico.nombre == "Armario"

    def test_material_property(self, armario_basico):
        """Prueba acceder al material."""
        assert armario_basico.material == "MDF"

    def test_color_property(self, armario_basico):
        """Prueba acceder al color."""
        assert armario_basico.color == "Blanco"

    def test_precio_base_property(self, armario_basico):
        """Prueba acceder al precio_base."""
        assert armario_basico.precio_base == 300


class TestArmarioCalcularPrecio:
    """Pruebas para el cálculo del precio."""

    def test_calcular_precio_basico(self):
        """Prueba cálculo de precio básico."""
        armario = Armario("Armario", "MDF", "Blanco", 200, num_puertas=2)
        # Precio = 200 + (2 puertas * 50) = 300
        precio = armario.calcular_precio()
        assert precio == 300

    @pytest.mark.parametrize("num_puertas,num_cajones,tiene_espejos,esperado", [
        (2, 0, False, 300),      # 200 + 100
        (3, 2, False, 460),      # 200 + 150 + 60
        (2, 0, True, 400),       # 200 + 100 + 100
        (4, 4, True, 620),       # 200 + 200 + 120 + 100
    ])
    def test_calcular_precio_componentes(self, num_puertas, num_cajones, tiene_espejos, esperado):
        """Prueba que cada componente afecta el precio."""
        armario = Armario(
            "Armario", "MDF", "Blanco", 200,
            num_puertas=num_puertas,
            num_cajones=num_cajones,
            tiene_espejos=tiene_espejos
        )
        precio = armario.calcular_precio()
        assert precio == esperado

    def test_precio_aumenta_con_puertas(self):
        """Prueba que más puertas aumentan el precio."""
        armario1 = Armario("Armario", "MDF", "Blanco", 200, num_puertas=2)
        armario2 = Armario("Armario", "MDF", "Blanco", 200, num_puertas=4)
        
        assert armario2.calcular_precio() > armario1.calcular_precio()

    def test_precio_aumenta_con_cajones(self):
        """Prueba que más cajones aumentan el precio."""
        armario1 = Armario("Armario", "MDF", "Blanco", 200, num_cajones=0)
        armario2 = Armario("Armario", "MDF", "Blanco", 200, num_cajones=3)
        
        assert armario2.calcular_precio() > armario1.calcular_precio()

    def test_precio_aumenta_con_espejos(self):
        """Prueba que tener espejos aumenta el precio."""
        armario1 = Armario("Armario", "MDF", "Blanco", 200, tiene_espejos=False)
        armario2 = Armario("Armario", "MDF", "Blanco", 200, tiene_espejos=True)
        
        assert armario2.calcular_precio() > armario1.calcular_precio()


class TestArmarioObtenerDescripcion:
    """Pruebas para el método obtener_descripcion."""

    def test_obtener_descripcion(self):
        """Prueba obtener descripción de armario."""
        armario = Armario(
            "Armario Moderno",
            "Madera",
            "Nogal",
            500,
            num_puertas=3,
            num_cajones=4,
            tiene_espejos=True
        )
        descripcion = armario.obtener_descripcion()
        
        assert isinstance(descripcion, str)
        assert "Armario Moderno" in descripcion
        assert "Madera" in descripcion
        assert "Nogal" in descripcion
        assert "3" in descripcion  # puertas
        assert "4" in descripcion  # cajones

    def test_obtener_descripcion_incluye_espejos(self):
        """Prueba que descripción menciona espejos."""
        armario = Armario(
            "Armario",
            "MDF",
            "Blanco",
            300,
            tiene_espejos=True
        )
        descripcion = armario.obtener_descripcion()
        
        assert "Sí" in descripcion or "espejos" in descripcion.lower()
