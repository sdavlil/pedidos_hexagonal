from pydantic import BaseModel

class Dinero(BaseModel):
    monto: float

    def es_valido(self):
        if self.monto < 0:
            raise ValueError("El monto no puede ser negativo")