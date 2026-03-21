from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.domain.use_cases.crear_pedido import CrearPedidoUseCase
from app.domain.use_cases.listar_pedidos import ListarPedidosUseCase
from app.domain.use_cases.actualizar_estado import ActualizarEstadoUseCase
from app.domain.use_cases.eliminar_pedido import EliminarPedidoUseCase
from app.domain.use_cases.catalogo import ObtenerCatalogoUseCase
from app.domain.use_cases.obtener_pedido import ObtenerPedidoUseCase
from app.domain.use_cases.detalle_pedido import ObtenerDetallePedidoUseCase

repo = SQLitePedidoRepository()

router = APIRouter()
templates = Jinja2Templates(directory="app/infrastructure/web/templates")

# =========================
# Instancias de casos de uso
# =========================

crear_pedido_uc = CrearPedidoUseCase(repo)
obtener_pedidos_uc = ListarPedidosUseCase(repo)
detalle_pedido_uc = ObtenerDetallePedidoUseCase(repo)
actualizar_estado_uc = ActualizarEstadoUseCase(repo)
eliminar_pedido_uc = EliminarPedidoUseCase(repo)
obtener_catalogo_uc = ObtenerCatalogoUseCase()


# =========================
# CATÁLOGO
# =========================
@router.get("/")
def catalogo(request: Request):
    catalogo = obtener_pedidos_uc.ejecutar()
    return templates.TemplateResponse(
        "catalogo.html",
        {"request": request, "catalogo": catalogo}
    )


# =========================
# CREAR PEDIDO
# =========================
@router.post("/crear")
def crear(cliente: str = Form(...), data: dict = Form(...)):

    # Pasamos todo al use case y él decide la validación, filtrado, total, etc.
    pedido = crear_pedido_uc.ejecutar(cliente=cliente, datos=data)

    if pedido and getattr(pedido, "id", None):
        return RedirectResponse(f"/pedidos?success_id={pedido.id}", status_code=303)

    return RedirectResponse("/pedidos", status_code=303)


# =========================
# VER PEDIDOS + FILTROS
# =========================
@router.get("/pedidos")
def ver_pedidos(request: Request, cliente: Optional[str] = None, pedido_id: Optional[str] = None, success_id: Optional[int] = None):

    pedidos = obtener_catalogo_uc.ejecutar(filtro_cliente=cliente, filtro_id=pedido_id)
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