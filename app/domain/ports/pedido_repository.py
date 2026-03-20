from abc import ABC, abstractmethod

class PedidoRepository(ABC):

    @abstractmethod
    def guardar(self, pedido):
        pass

    @abstractmethod
    def obtener_todos(self):
        pass