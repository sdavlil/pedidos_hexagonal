from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Pedido:
    id: int
    cliente: str
    items: List[Dict]
    total: float
    estado: str = "CREADO"

    def actualizar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado
