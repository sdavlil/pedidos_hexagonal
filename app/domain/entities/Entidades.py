from pydantic import BaseModel, field_validator
from app.domain.exceptions.Excepciones_Dominio import PedidoVacioError
from typing import List

class Producto(BaseModel):
    nombre: str
    precio: float
    cantidad: int

    @field_validator("cantidad")
    def cantidad_mayor_a_cero(cls, v):
        if v <= 0:
            raise PedidoVacioError("La cantidad debe ser mayor a 0")
        return v


class Pedido(BaseModel):
    cliente: str
    productos: List[Producto]

    def total(self) -> float:
        return sum(p.precio * p.cantidad for p in self.productos)

    def validar(self):
        if not self.productos:
            raise ValueError("El pedido debe tener al menos un producto")