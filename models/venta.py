class Venta:

    def __init__(
        self,
        id_venta,
        id_usuario,
        id_cliente,
        fecha_venta,
        metodo_pago,
        iva,
        total,
        estado
    ):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.fecha_venta = fecha_venta
        self.metodo_pago = metodo_pago
        self.iva = iva
        self.total = total
        self.estado = estado

    def mostrar_info(self):
        return (
            f"Venta: {self.id_venta} - "
            f"Cliente: {self.id_cliente} - "
            f"Fecha: {self.fecha_venta} - "
            f"Total: ${self.total:.2f} - "
            f"Estado: {self.estado}"
        )