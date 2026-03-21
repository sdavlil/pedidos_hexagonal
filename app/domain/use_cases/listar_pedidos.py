class ListarPedidosUseCase:

    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self):
        return self.repo.obtener_todos()