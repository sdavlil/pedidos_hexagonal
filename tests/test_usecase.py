from app.domain.use_cases.crear_pedido import CrearPedidoUseCase
from app.domain.entities.pedido import Pedido, Producto
import pytest
from app.domain.exceptions.pedido_error import PedidoError

# =========================
# FAKE REPO
# =========================
class FakeRepo:
    def __init__(self):
        self.guardado = False

    def guardar(self, pedido):
        self.guardado = True


# =========================
# TEST USE CASE
# =========================
def test_crear_pedido():
    repo = FakeRepo()
    usecase = CrearPedidoUseCase(repo)

    pedido = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=1)]
    )

    usecase.ejecutar(pedido)

    assert repo.guardado is True


# =========================
# TEST USECASE FALLA VALIDACIÓN
# =========================
def test_usecase_error_validacion():
    repo = FakeRepo()
    usecase = CrearPedidoUseCase(repo)

    pedido = Pedido(cliente="Juan", productos=[])

    with pytest.raises(PedidoError):
        usecase.ejecutar(pedido)


# =========================
# TEST USECASE GUARDA UNA VEZ
# =========================
def test_usecase_llama_repo():
    class FakeRepoCount:
        def __init__(self):
            self.count = 0

        def guardar(self, pedido):
            self.count += 1

    repo = FakeRepoCount()
    usecase = CrearPedidoUseCase(repo)

    pedido = Pedido(
        cliente="Juan",
        productos=[Producto(nombre="iPhone", precio=1000, cantidad=1)]
    )

    usecase.ejecutar(pedido)

    assert repo.count == 1