from abc import ABC, abstractmethod
from typing import List
from app.domain.pedido import Pedido

class PedidoRepositoryPort(ABC):

    @abstractmethod
    def guardar(self, pedido: Pedido):
        pass

    @abstractmethod
    def obtener_por_id(self, pedido_id: int) -> Pedido:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Pedido]:
        pass

    @abstractmethod
    def eliminar(self, pedido_id: int):
        pass


