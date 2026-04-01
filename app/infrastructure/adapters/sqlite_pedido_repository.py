import json
from app.application.ports import PedidoRepositoryPort
from app.domain.pedido import Pedido
from app.infrastructure.repositories.database import SessionLocal
from app.infrastructure.repositories.models import PedidoModel



class SQLitePedidoRepository(PedidoRepositoryPort):

    # =========================
    # GUARDAR (CREAR O ACTUALIZAR)
    # =========================
    def guardar(self, pedido: Pedido):
        db = SessionLocal()

        # Si ya tiene ID → actualizar
        if pedido.id:
            db_pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido.id).first()

            if db_pedido:
                db_pedido.cliente = pedido.cliente
                db_pedido.items = json.dumps(pedido.items)
                db_pedido.total = pedido.total
                db_pedido.estado = pedido.estado

                db.commit()
                db.refresh(db_pedido)
                db.close()
                return db_pedido.id

        # Si no tiene ID → crear nuevo
        nuevo_pedido = PedidoModel(
            cliente=pedido.cliente,
            items=json.dumps(pedido.items),
            total=pedido.total,
            estado=pedido.estado
        )

        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)
        db.close()

        return nuevo_pedido.id


    # =========================
    # OBTENER POR ID
    # =========================
    def obtener_por_id(self, pedido_id: int):
        db = SessionLocal()

        pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

        db.close()

        if not pedido:
            return None

        return Pedido(
            id=pedido.id,
            cliente=pedido.cliente,
            items=json.loads(pedido.items),
            total=pedido.total,
            estado=pedido.estado
        )


    # =========================
    # OBTENER TODOS
    # =========================
    def obtener_todos(self):
        db = SessionLocal()

        pedidos = db.query(PedidoModel).all()

        db.close()

        return [
            Pedido(
                id=p.id,
                cliente=p.cliente,
                items=json.loads(p.items),
                total=p.total,
                estado=p.estado
            )
            for p in pedidos
        ]


    # =========================
    # ELIMINAR
    # =========================
    def eliminar(self, pedido_id: int):
        db = SessionLocal()

        pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

        if pedido:
            db.delete(pedido)
            db.commit()

        db.close()
    def actualizar_estado(self, pedido_id: int, estado: str):
        db = SessionLocal()

        pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

        if not pedido:
            db.close()
            raise ValueError("Pedido no encontrado")

        pedido.estado = estado

        db.commit()
        db.refresh(pedido)
        db.close()

        return pedido