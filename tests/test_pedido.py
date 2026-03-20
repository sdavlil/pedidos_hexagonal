import pytest
from app.domain.entities.pedido import Pedido, Producto

def test_total_correcto():
    pedido = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=2)]
    )
    assert pedido.total() == 2000


def test_pedido_vacio():
    with pytest.raises(ValueError):
        Pedido(cliente="Juan", productos=[]).validar()