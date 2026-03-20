def test_cantidad_invalida():
    with pytest.raises(ValueError):
        Producto(nombre="iPhone", precio=1000, cantidad=0)