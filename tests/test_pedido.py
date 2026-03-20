import pytest
from app.domain.entities.pedido import Pedido, Producto, PedidoError

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
# TEST PEDIDO VACÍO (VALIDACIÓN)
# =========================
def test_pedido_vacio():
    with pytest.raises(ValueError):
        Pedido(cliente="Juan", productos=[]).validar()


# =========================
# TEST TOTAL (REUTILIZANDO PEDIDO)
# =========================
def test_total_multiple_productos():
    pedido = Pedido(
        cliente="Ana",
        productos=[
            Producto(nombre="iPhone", precio=1000, cantidad=2),
            Producto(nombre="MacBook", precio=2000, cantidad=1)
        ]
    )
    assert pedido.total() == 4000  # 1000*2 + 2000*1 = 4000


# =========================
# TEST PEDIDO CON ERROR PERSONALIZADO
# =========================
def test_pedido_error():
    with pytest.raises(PedidoError):
        # Supongamos que PedidoError se lanza si hay un producto con precio negativo
        Pedido(cliente="Carlos", productos=[Producto(nombre="X", precio=-100, cantidad=1)]).validar()


# =========================
# FAKE REPOSITORIO PARA TEST
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