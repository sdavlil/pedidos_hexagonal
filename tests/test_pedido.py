import pytest
from app.domain.entities.pedido import Pedido, Producto
from app.domain.exceptions.pedido_error import PedidoError, PedidoVacioError

# =========================
# TEST TOTAL CORRECTO
# =========================
def test_total_correcto():
    pedido = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=2)]
    )
    assert pedido.total() == 2000


# =========================
# TEST PEDIDO VACÍO
# =========================
def test_pedido_vacio():
    with pytest.raises(PedidoVacioError):
        Pedido(cliente="Juan", productos=[]).validar()


# =========================
# TEST TOTAL MÚLTIPLES PRODUCTOS
# =========================
def test_total_multiple_productos():
    pedido = Pedido(
        cliente="Ana",
        productos=[
            Producto(nombre="iPhone", precio=1000, cantidad=2),
            Producto(nombre="MacBook", precio=2000, cantidad=1)
        ]
    )
    assert pedido.total() == 4000


# =========================
# TEST ERROR DE DOMINIO (precio inválido)
# =========================
def test_pedido_error_precio_negativo():
    with pytest.raises(PedidoError):
        Pedido(
            cliente="Carlos",
            productos=[Producto(nombre="X", precio=-100, cantidad=1)]
        ).validar()


# =========================
# FAKE REPO TEST
# =========================
class FakeRepo:
    def __init__(self):
        self.ok = False

    def guardar(self, pedido):
        self.ok = True


def test_fake_repo_guardar():
    repo = FakeRepo()
    pedido = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=1)]
    )
    repo.guardar(pedido)
    assert repo.ok is True

# =========================
# TEST NOMBRE VACÍO
# =========================
def test_nombre_vacio():
    with pytest.raises(PedidoError):
        Producto(nombre="", precio=1000, cantidad=1)

# =========================
# TEST CLIENTE VACÍO
# =========================
def test_cliente_vacio():
    with pytest.raises(PedidoError):
        Pedido(cliente="", productos=[
            Producto(nombre="iPhone", precio=1000, cantidad=1)
        ]).validar()


# =========================
# TEST PRODUCTOS NONE
# =========================
def test_productos_none():
    with pytest.raises(PedidoError):
        Pedido(cliente="Juan", productos=None).validar()


# =========================
# TEST TOTAL CERO
# =========================
def test_total_cero():
    pedido = Pedido(cliente="Juan", productos=[
        Producto(nombre="iPhone", precio=0, cantidad=1)
    ])
    assert pedido.total() == 0


# =========================
# TEST MUCHOS PRODUCTOS
# =========================
def test_muchos_productos():
    pedido = Pedido(
        cliente="Juan",
        productos=[
            Producto(nombre="A", precio=100, cantidad=1),
            Producto(nombre="B", precio=200, cantidad=2),
            Producto(nombre="C", precio=300, cantidad=3),
        ]
    )
    assert pedido.total() == 100 + 400 + 900

# =========================
# TEST VALORES GRANDES
# =========================
def test_total_grandes_valores():
    pedido = Pedido(
        cliente="Empresa",
        productos=[Producto(nombre="Servidor", precio=1000000, cantidad=2)]
    )
    assert pedido.total() == 2000000