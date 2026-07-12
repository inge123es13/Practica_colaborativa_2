class Producto:
    def __init__(self, id_producto=None, nombre="", descripcion="", precio=0.0, stock_actual=0, marca="", talla="", id_categoria=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock_actual = stock_actual
        self.marca = marca
        self.talla = talla
        self.id_categoria = id_categoria