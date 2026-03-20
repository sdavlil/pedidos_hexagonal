from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

# Importar tus casos de uso (use cases) en vez de service directo
from app.application.pedido_usecases import (
    CrearPedidoUseCase,
    ObtenerCatalogoUseCase,
    ObtenerPedidosUseCase,
    ObtenerDetallePedidoUseCase,
    ActualizarEstadoUseCase,
    EliminarPedidoUseCase
)

router = APIRouter()
templates = Jinja2Templates(directory="app/infrastructure/web/templates")

# =========================
# Instancias de casos de uso
# =========================
crear_pedido_uc = CrearPedidoUseCase()
obtener_catalogo_uc = ObtenerCatalogoUseCase()
obtener_pedidos_uc = ObtenerPedidosUseCase()
detalle_pedido_uc = ObtenerDetallePedidoUseCase()
actualizar_estado_uc = ActualizarEstadoUseCase()
eliminar_pedido_uc = EliminarPedidoUseCase()


# =========================
# CATÁLOGO
# =========================
@router.get("/")
def catalogo(request: Request):

    # Antes: catalogo = service.obtener_catalogo()
    # Ahora usando use case
    catalogo = obtener_catalogo_uc.ejecutar()

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

    # Antes: catalogo = service.obtener_catalogo()
    catalogo = obtener_catalogo_uc.ejecutar()

    items = []

    if not isinstance(producto_ids, list):
        producto_ids = [producto_ids]

    if not isinstance(cantidades, list):
        cantidades = [cantidades]

    for pid, cantidad in zip(producto_ids, cantidades):

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

    # Antes: pedido = service.crear_pedido(cliente=cliente, items=items)
    pedido = crear_pedido_uc.ejecutar(cliente=cliente, items=items)

    if pedido and getattr(pedido, "id", None):
        return RedirectResponse(f"/pedidos?success_id={pedido.id}", status_code=303)

    return RedirectResponse("/pedidos", status_code=303)


# =========================
# VER PEDIDOS + FILTROS
# =========================
@router.get("/pedidos")
def ver_pedidos(
    request: Request,
    cliente: Optional[str] = None,
    pedido_id: Optional[str] = None,
    success_id: Optional[int] = None
):

    pedidos = obtener_pedidos_uc.ejecutar()

    if cliente and cliente.strip() != "":
        pedidos = [
            p for p in pedidos
            if cliente.lower() in p.cliente.lower()
        ]

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

    pedido = detalle_pedido_uc.ejecutar(pedido_id)

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

    if estado.strip() == "":
        return RedirectResponse(f"/pedidos/{pedido_id}", status_code=303)

    actualizar_estado_uc.ejecutar(pedido_id, estado)

    return RedirectResponse(f"/pedidos/{pedido_id}", status_code=303)


# =========================
# ELIMINAR PEDIDO
# =========================
@router.post("/eliminar/{pedido_id}")
def eliminar_pedido(pedido_id: int):

    eliminar_pedido_uc.ejecutar(pedido_id)

    return RedirectResponse("/pedidos?deleted=1", status_code=303)