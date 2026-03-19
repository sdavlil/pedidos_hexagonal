from app.application.ports import PedidoRepositoryPort
from app.domain.producto import Producto
from app.domain.pedido import Pedido

from typing import List

class GestionadorPedidos:

    def __init__(self, repository: PedidoRepositoryPort):
        self.repository = repository

    def crear_pedido(self, cliente: str, items: list):
        total = sum(item["precio"] * item["cantidad"] for item in items)

        pedido = Pedido(
            id=None,
            cliente=cliente,
            items=items,
            total=total
        )

        nuevo_id = self.repository.guardar(pedido)
        pedido.id = nuevo_id

        return pedido


    def obtener_pedido(self, pedido_id: int):
        return self.repository.obtener_por_id(pedido_id)

    def obtener_todos(self):
        return self.repository.obtener_todos()

    def obtener_catalogo(self):
        return [
            Producto(1, "iPhone 17 Pro Max", 1200, "/static/iphone.jpg"),
            Producto(2, "MacBook Pro M4", 1800, "/static/macbook.jpg"),
            Producto(3, "iPad Pro", 1000, "/static/ipad.jpg"),
            Producto(4, "Apple Watch Series 9", 600, "/static/watch.jpg"),
            Producto(5, "AirPods Pro", 300, "/static/airpods.jpg"),
        ]

    def actualizar_estado(self, pedido_id: int, nuevo_estado: str):
        pedido = self.repository.obtener_por_id(pedido_id)

        if not pedido:
            return None

        pedido.actualizar_estado(nuevo_estado)
        self.repository.guardar(pedido)
        return pedido


    def eliminar_pedido(self, pedido_id: int):
        self.repository.eliminar(pedido_id)

