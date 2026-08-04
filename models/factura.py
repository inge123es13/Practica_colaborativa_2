class Factura:

    def __init__(
        self,
        id_factura=0,
        id_venta=0,
        id_cliente=0,
        fecha_factura=None,
        folio="",
        estado="Emitida"
    ):
        self.id_factura = id_factura
        self.id_venta = id_venta
        self.id_cliente = id_cliente
        self.fecha_factura = fecha_factura
        self.folio = folio
        self.estado = estado