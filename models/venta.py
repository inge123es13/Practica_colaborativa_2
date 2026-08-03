class Venta:

    def __init__(
        self,
        id_venta=0,
        id_usuario=0,
        id_cliente=0,
        id_producto=0,
        fecha_venta=None,
        metodo_pago="Efectivo",
        cantidad=1,
        precio_unitario=0,
        subtotal=0,
        iva=0,
        total=0,
        estado="Pagada"
    ):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.id_producto = id_producto
        self.fecha_venta = fecha_venta
        self.metodo_pago = metodo_pago
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.estado = estado