import pytest
from app.domain.entities.pedido import Pedido, Producto


def test_pedido_valido():
    p = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=1)]
    )
    assert p.total() == 1000


def test_pedido_sin_productos():
    with pytest.raises(ValueError):
        Pedido(cliente="Juan", productos=[]).validar()


def test_cantidad_invalida():
    with pytest.raises(ValueError):
        Producto(nombre="iPhone", precio=1000, cantidad=0)