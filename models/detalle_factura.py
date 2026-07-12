class DetalleFactura:
    def __init__(self, id_detalle, cantidad, precio_unitario, subtotal, id_factura, id_producto):
        self.id_detalle = id_detalle
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.id_factura = id_factura    # Llave foránea vinculada a Facturas (FK)
        self.id_producto = id_producto  # Llave foránea vinculada a Productos (FK)

    def __str__(self):
        return f"Detalle {self.id_detalle} | Prod ID: {self.id_producto} | Cantidad: {self.cantidad} | Subtotal: ${self.subtotal}"