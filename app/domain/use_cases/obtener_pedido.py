class ObtenerPedidoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, pedido_id: int):
        return self.repo.obtener_por_id(pedido_id)