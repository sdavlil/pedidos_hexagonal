class ActualizarEstadoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, pedido_id, estado):
        return self.repo.actualizar_estado(pedido_id, estado)