class EliminarPedidoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, pedido_id):
        self.repo.eliminar(pedido_id)