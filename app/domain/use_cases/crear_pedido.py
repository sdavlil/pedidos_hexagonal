class CrearPedidoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, pedido):
        pedido.validar()
        self.repo.guardar(pedido)