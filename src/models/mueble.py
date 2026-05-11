from abc import ABC, abstractmethod

class Mueble(ABC):
    def __init__(self, nombre: str, material: str, color: str, precio_base: float):
        # Usar setters para que se apliquen validaciones desde el inicio
        self.nombre = nombre
        self.material = material
        self.color = color
        self.precio_base = precio_base

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = " ".join(value.split())

    @property
    def material(self) -> str:
        return self._material

    @material.setter
    def material(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El material no puede estar vacío")
        self._material = value.strip()

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El color no puede estar vacío")
        self._color = value.strip()

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, value: float) -> None:
        if value < 0:
            raise ValueError("El precio base no puede ser negativo")
        if value == 0:
            raise ValueError("El precio base debe ser mayor que cero")
        self._precio_base = value

    @abstractmethod
    def calcular_precio(self) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.nombre} de {self.material} en color {self.color}"

    def __repr__(self) -> str:
        return f"Mueble(nombre='{self.nombre}', material='{self.material}', color='{self.color}', precio_base={self.precio_base})"
