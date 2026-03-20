from fastapi import APIRouter, Depends
from typing import List
from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from app.domain.use_cases.crear_pedido import CrearPedidoUseCase
from app.domain.use_cases.listar_pedidos import ListarPedidosUseCase
from app.domain.use_cases.actualizar_estado import ActualizarEstadoUseCase
from app.domain.use_cases.eliminar_pedido import EliminarPedidoUseCase
from app.domain.pedido import Pedido

router = APIRouter()

# =========================
# Instancias de repositorio y use cases
# =========================
repo = SQLitePedidoRepository()

crear_pedido_uc = CrearPedidoUseCase(repo)
listar_pedidos_uc = ListarPedidosUseCase(repo)
actualizar_estado_uc = ActualizarEstadoUseCase(repo)
eliminar_pedido_uc = EliminarPedidoUseCase(repo)


# =========================
# CREAR PEDIDO
# =========================
@router.post("/pedidos")
def crear_pedido(data: dict):
    pedido = Pedido(
        id=data["id"],
        cliente=data["cliente"],
        items=data["items"],
        total=data["total"]
    )

    # Use case ejecuta toda la lógica y persiste
    crear_pedido_uc.ejecutar(pedido)

    return {"mensaje": "Pedido creado", "pedido": pedido.__dict__}


# =========================
# LISTAR PEDIDOS
# =========================
@router.get("/pedidos")
def listar_pedidos():
    pedidos: List[Pedido] = listar_pedidos_uc.ejecutar()
    return [p.__dict__ for p in pedidos]


# =========================
# ACTUALIZAR ESTADO
# =========================
@router.put("/pedidos/{pedido_id}")
def actualizar_estado(pedido_id: int, data: dict):
    pedido = actualizar_estado_uc.ejecutar(pedido_id, data["estado"])
    return {"mensaje": "Pedido actualizado", "pedido": pedido.__dict__}


# =========================
# ELIMINAR PEDIDO
# =========================
@router.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    eliminar_pedido_uc.ejecutar(pedido_id)
    return {"mensaje": "Pedido eliminado"}