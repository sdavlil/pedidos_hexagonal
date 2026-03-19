from fastapi import APIRouter
from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from app.application.pedido_service import GestionadorPedidos

router = APIRouter()
repo = SQLitePedidoRepository()
service = GestionadorPedidos(repo)

@router.post("/pedidos")
def crear_pedido(data: dict):
    pedido = service.crear_pedido(
        id=data["id"],
        cliente=data["cliente"],
        items=data["items"],
        total=data["total"]
    )
    return {"mensaje": "Pedido creado", "pedido": pedido.__dict__}

@router.get("/pedidos")
def listar_pedidos():
    pedidos = service.obtener_todos()
    return [p.__dict__ for p in pedidos]

@router.put("/pedidos/{pedido_id}")
def actualizar_estado(pedido_id: int, data: dict):
    pedido = service.actualizar_estado(pedido_id, data["estado"])
    return {"mensaje": "Pedido actualizado", "pedido": pedido.__dict__}

@router.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    service.eliminar_pedido(pedido_id)
    return {"mensaje": "Pedido eliminado"}
