from app.domain.pedido import Pedido

class ObtenerDetallePedidoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, pedido_id: int) -> Pedido:
        return self.repo.obtener_por_id(pedido_id)