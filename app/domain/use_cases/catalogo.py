from app.domain.producto import Producto
class ObtenerCatalogoUseCase:

    def ejecutar(self):
        return [
            Producto(1, "iPhone 17 Pro Max", 1200, "/static/iphone.jpg"),
            Producto(2, "MacBook Pro M4", 1800, "/static/macbook.jpg"),
            Producto(3, "iPad Pro", 1000, "/static/ipad.jpg"),
            Producto(4, "Apple Watch Series 9", 600, "/static/watch.jpg"),
            Producto(5, "AirPods Pro", 300, "/static/airpods.jpg"),
        ]