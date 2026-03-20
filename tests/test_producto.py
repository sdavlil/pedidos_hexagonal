import pytest
from app.domain.entities.pedido import Producto
from app.domain.exceptions.pedido_error import CantidadInvalidaError
from app.domain.exceptions.pedido_error import PedidoError

def test_cantidad_invalida():
    with pytest.raises(CantidadInvalidaError):
        Producto(nombre="iPhone", precio=1000, cantidad=0)

# =========================
# TEST PRECIO NEGATIVO
# =========================

def test_precio_negativo():
    with pytest.raises(PedidoError):
        Producto(nombre="iPhone", precio=-100, cantidad=1)

# =========================
# TEST NOMBRE VACÍO
# =========================
def test_nombre_vacio():
    with pytest.raises(PedidoError):
        Producto(nombre="", precio=1000, cantidad=1)       
