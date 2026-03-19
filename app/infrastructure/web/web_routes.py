from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from app.application.pedido_service import GestionadorPedidos

router = APIRouter()
templates = Jinja2Templates(directory="app/infrastructure/web/templates")

repo = SQLitePedidoRepository()
service = GestionadorPedidos(repo)


# =========================
# CATÁLOGO
# =========================
@router.get("/")
def catalogo(request: Request):
    catalogo = service.obtener_catalogo()
    return templates.TemplateResponse(
        "catalogo.html",
        {
            "request": request,
            "catalogo": catalogo
        }
    )


# =========================
# CREAR PEDIDO
# =========================
@router.post("/crear")
def crear(
    cliente: str = Form(...),
    producto_ids: list[str] = Form(default=[]),
    cantidades: list[str] = Form(default=[])
):
    catalogo = service.obtener_catalogo()
    items = []

    # Seguridad extra: si no llegan listas, convertir
    if not isinstance(producto_ids, list):
        producto_ids = [producto_ids]

    if not isinstance(cantidades, list):
        cantidades = [cantidades]

    for pid, cantidad in zip(producto_ids, cantidades):

        # Evitar valores vacíos o inválidos
        if not cantidad or not cantidad.isdigit():
            continue

        cantidad = int(cantidad)

        if cantidad > 0:
            producto = next((p for p in catalogo if str(p.id) == str(pid)), None)

            if producto:
                items.append({
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "cantidad": cantidad
                })

    if not items:
        return RedirectResponse("/", status_code=303)

    pedido = service.crear_pedido(cliente=cliente, items=items)

    if pedido and pedido.id:
        return RedirectResponse(f"/pedidos?success_id={pedido.id}", status_code=303)

    return RedirectResponse("/pedidos", status_code=303)


# =========================
# VER PEDIDOS + FILTROS
# =========================
from typing import Optional

@router.get("/pedidos")
def ver_pedidos(
    request: Request,
    cliente: Optional[str] = None,
    pedido_id: Optional[str] = None,
    success_id: Optional[int] = None
):
    pedidos = service.obtener_todos()

    # Filtrar por cliente si tiene valor
    if cliente and cliente.strip() != "":
        pedidos = [
            p for p in pedidos
            if cliente.lower() in p.cliente.lower()
        ]

    # Filtrar por ID solo si es número válido
    if pedido_id and pedido_id.strip().isdigit():
        pedido_id_int = int(pedido_id)
        pedidos = [
            p for p in pedidos
            if p.id == pedido_id_int
        ]

    return templates.TemplateResponse(
        "pedidos.html",
        {
            "request": request,
            "pedidos": pedidos,
            "success_id": success_id
        }
    )


# =========================
# DETALLE PEDIDO
# =========================
@router.get("/pedidos/{pedido_id}")
def detalle_pedido(request: Request, pedido_id: int):
    pedido = service.obtener_pedido(pedido_id)

    if not pedido:
        return RedirectResponse("/pedidos", status_code=303)

    return templates.TemplateResponse(
        "detalle.html",
        {
            "request": request,
            "pedido": pedido
        }
    )


# =========================
# ACTUALIZAR ESTADO
# =========================
@router.post("/actualizar_estado/{pedido_id}")
def actualizar_estado(pedido_id: int, estado: str = Form(...)):

    # No actualizar si selecciona opción vacía
    if estado.strip() == "":
        return RedirectResponse(f"/pedidos/{pedido_id}", status_code=303)

    service.actualizar_estado(pedido_id, estado)

    return RedirectResponse(f"/pedidos/{pedido_id}", status_code=303)


# =========================
# ELIMINAR PEDIDO
# =========================
@router.post("/eliminar/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    service.eliminar_pedido(pedido_id)
    return RedirectResponse("/pedidos?deleted=1", status_code=303)
