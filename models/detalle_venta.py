class DetalleVenta:

    def __init__(
        self,
        id_detalle,
        id_venta,
        id_producto,
        cantidad,
        subtotal
    ):
        self.id_detalle = id_detalle
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal = subtotal

    def mostrar_info(self):
        return (
            f"Detalle: {self.id_detalle} - "
            f"Venta: {self.id_venta} - "
            f"Producto: {self.id_producto} - "
            f"Cantidad: {self.cantidad} - "
            f"Subtotal: ${self.subtotal}"
        )