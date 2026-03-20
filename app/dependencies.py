from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from app.application.pedido_service import GestionadorPedidos

def get_pedido_service():
    repo = SQLitePedidoRepository()
    return GestionadorPedidos(repo)