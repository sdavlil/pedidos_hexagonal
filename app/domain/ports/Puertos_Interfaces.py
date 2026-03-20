from abc import ABC, abstractmethod

class PedidoRepository(ABC):

    @abstractmethod
    def guardar(self, pedido):
        pass

    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def actualizar_estado(self, pedido_id, estado):
        pass

    @abstractmethod
    def eliminar(self, pedido_id):
        pass