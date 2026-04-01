from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi import Query
from fastapi.templating import Jinja2Templates
from typing import List
from app.infrastructure.adapters.sqlite_pedido_repository import SQLitePedidoRepository
from app.domain.use_cases.crear_pedido import CrearPedidoUseCase
from app.domain.use_cases.listar_pedidos import ListarPedidosUseCase
from app.domain.use_cases.actualizar_estado import ActualizarEstadoUseCase
from app.domain.use_cases.eliminar_pedido import EliminarPedidoUseCase
from app.domain.pedido import Pedido
from fastapi.responses import RedirectResponse
import uuid


templates = Jinja2Templates(directory="app/infrastructure/web/templates")


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
from fastapi import Form
from fastapi.responses import RedirectResponse
import uuid

@router.post("/crear")
def crear_pedido_form(
    cliente: str = Form(...),
    productos: List[str] = Form(...),
    precios: List[float] = Form(...),
    cantidades: List[int] = Form(...)
):
    items = []
    total = 0

    for i in range(len(productos)):
        if cantidades[i] > 0:
            subtotal = precios[i] * cantidades[i]
            total += subtotal

            items.append({
                "nombre": productos[i],
                "precio": precios[i],
                "cantidad": cantidades[i]
            })

    pedido = Pedido(
        id=str(uuid.uuid4()),
        cliente=cliente,
        items=items,
        total=total
    )

    crear_pedido_uc.ejecutar(pedido)

    return RedirectResponse(url="/pedidos?success=1", status_code=303)
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
def listar(
    request: Request,
    pedido_id: str = Query(None),
    cliente: str = Query(None)
):
    print("ID:", pedido_id)
    print("CLIENTE:", cliente)

    pedidos: List[Pedido] = listar_pedidos_uc.ejecutar()

    if pedido_id:
        pedidos = [p for p in pedidos if str(p.id) == str(pedido_id)]

    if cliente:
        pedidos = [p for p in pedidos if cliente.lower() in p.cliente.lower()]

    return templates.TemplateResponse("pedidos.html", {
        "request": request,
        "pedidos": pedidos,
        "success_id": request.query_params.get("success")
    })

# =========================
# ACTUALIZAR ESTADO
# =========================
@router.post("/actualizar_estado/{pedido_id}")
def actualizar_estado(pedido_id: int, estado: str = Form(...)):
    pedido = actualizar_estado_uc.ejecutar(pedido_id, estado)
    return RedirectResponse(url=f"/pedidos/{pedido_id}", status_code=303)


# =========================
# ELIMINAR PEDIDO
# =========================
@router.post("/eliminar/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    eliminar_pedido_uc.ejecutar(pedido_id)
    return RedirectResponse(url="/pedidos?deleted=1", status_code=303)