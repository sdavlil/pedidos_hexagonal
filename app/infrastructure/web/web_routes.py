from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from typing import List
from fastapi import Request
from app.domain.use_cases.crear_pedido import CrearPedidoUseCase
from app.domain.use_cases.listar_pedidos import ListarPedidosUseCase
from app.domain.use_cases.actualizar_estado import ActualizarEstadoUseCase
from app.domain.use_cases.eliminar_pedido import EliminarPedidoUseCase
from app.domain.use_cases.catalogo import ObtenerCatalogoUseCase
from app.domain.use_cases.detalle_pedido import ObtenerDetallePedidoUseCase

# =========================
# INIT
# =========================
repo = SQLitePedidoRepository()

router = APIRouter()
templates = Jinja2Templates(directory="app/infrastructure/web/templates")

# =========================
# USE CASES
# =========================
crear_pedido_uc = CrearPedidoUseCase(repo)
listar_pedidos_uc = ListarPedidosUseCase(repo)
detalle_pedido_uc = ObtenerDetallePedidoUseCase(repo)
actualizar_estado_uc = ActualizarEstadoUseCase(repo)
eliminar_pedido_uc = EliminarPedidoUseCase(repo)
catalogo_uc = ObtenerCatalogoUseCase()

# =========================
# CATÁLOGO
# =========================
@router.get("/")
def catalogo(request: Request):
    catalogo = catalogo_uc.ejecutar()
    return templates.TemplateResponse(
        "catalogo.html",
        {"request": request, "catalogo": catalogo}
    )

# =========================
# CREAR PEDIDO
# =========================
from fastapi import Request

# =========================
# VER PEDIDOS
# =========================
@router.get("/pedidos")
def ver_pedidos(
    request: Request,
    success_id: Optional[int] = None
):
    pedidos = listar_pedidos_uc.ejecutar()

    return templates.TemplateResponse(
        "pedidos.html",
        {"request": request, "pedidos": pedidos, "success_id": success_id}
    )

# =========================
# DETALLE PEDIDO
# =========================
@router.get("/pedidos/{pedido_id}")
def detalle_pedido(request: Request, pedido_id: int):
    pedido = detalle_pedido_uc.ejecutar(pedido_id)

    if not pedido:
        return RedirectResponse("/pedidos", status_code=303)

    return templates.TemplateResponse(
        "detalle.html",
        {"request": request, "pedido": pedido}
    )

# =========================
# ACTUALIZAR ESTADO
# =========================
@router.post("/actualizar_estado/{pedido_id}")
def actualizar_estado(pedido_id: int, estado: str = Form(...)):
    if estado.strip():
        actualizar_estado_uc.ejecutar(pedido_id, estado)

    return RedirectResponse(f"/pedidos/{pedido_id}", status_code=303)

# =========================
# ELIMINAR PEDIDO
# =========================
@router.post("/eliminar/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    eliminar_pedido_uc.ejecutar(pedido_id)
    return RedirectResponse("/pedidos?deleted=1", status_code=303)