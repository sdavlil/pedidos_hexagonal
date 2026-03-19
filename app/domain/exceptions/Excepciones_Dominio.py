class PedidoError(Exception):
    pass


class PedidoVacioError(PedidoError):
    def __init__(self):
        super().__init__("El pedido debe tener al menos un producto")


class CantidadInvalidaError(PedidoError):
    def __init__(self):
        super().__init__("La cantidad debe ser mayor a 0")