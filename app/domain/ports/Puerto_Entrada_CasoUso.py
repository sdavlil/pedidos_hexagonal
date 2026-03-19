class CrearPedidoUseCase:

    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido):
        pedido.validar()
        self.repo.guardar(pedido)