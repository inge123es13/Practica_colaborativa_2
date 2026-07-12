class Factura:
    def __init__(self, id_factura, fecha_factura, subtotal, iva, total, metodo_pago, estado, id_usuario):
        self.id_factura = id_factura
        self.fecha_factura = fecha_factura
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.metodo_pago = metodo_pago
        self.estado = estado  # (pendiente/pagada/cancelada)
        self.id_usuario = id_usuario  # Llave foránea vinculada al Usuario que realiza la compra

    def __str__(self):
        return f"Factura {self.id_factura} | Total: ${self.total} | Estado: {self.estado}"