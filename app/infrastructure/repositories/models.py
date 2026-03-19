from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.repositories.database import Base

class PedidoModel(Base):
    __tablename__ = "pedidos"

    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente = Column(String)
    items = Column(String)
    total = Column(Float)
    estado = Column(String)
