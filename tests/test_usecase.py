class FakeRepo:
    def guardar(self, pedido):
        self.guardado = True

def test_crear_pedido():
    repo = FakeRepo()
    usecase = CrearPedidoUseCase(repo)

    pedido = Pedido(cliente="Juan", productos=[...])

    usecase.ejecutar(pedido)

    assert repo.guardado == True