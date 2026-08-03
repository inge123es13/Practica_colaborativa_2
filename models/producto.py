class Producto:

    def __init__(
        self,
        id_producto,
        nombre,
        descripcion,
        precio,
        stock_actual,
        marca,
        talla,
        id_categoria
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock_actual = stock_actual
        self.marca = marca
        self.talla = talla
        self.id_categoria = id_categoria

    def mostrar_info(self):
        return (
            f"{self.id_producto} - {self.nombre} - "
            f"{self.marca} - Talla: {self.talla} - "
            f"Precio: ${self.precio} - Stock: {self.stock_actual}"
        )

    def actualizar_stock(self, cantidad):
        self.stock_actual = cantidad