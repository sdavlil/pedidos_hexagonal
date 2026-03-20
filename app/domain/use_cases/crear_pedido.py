class CrearPedidoUseCase:

    def __init__(self, repo):
        self.repo = repo

def ejecutar(self, pedido):
    pedido.validar()
    return self.repo.guardar(pedido)