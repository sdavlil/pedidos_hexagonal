class Pedido:
    def __init__(self, id, cliente, items, total, estado="CREADO"):
        self.id = id
        self.cliente = cliente
        self.items = items
        self.total = total
        self.estado = estado

    def validar(self):
        if not self.cliente:
            raise ValueError("El cliente es obligatorio")
        if not self.items:
            raise ValueError("Debe haber al menos un producto")
        if self.total <= 0:
            raise ValueError("El total debe ser mayor a 0")

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado