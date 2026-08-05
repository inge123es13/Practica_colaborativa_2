import flet as ft

from datetime import date
from decimal import Decimal, InvalidOperation

from dao.cliente_dao import ClienteDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO

from models.detalle_venta import DetalleVenta
from models.venta import Venta


def ventas_view(regresar, usuario_actual):

    # ---------- DAO ----------

    producto_dao = ProductoDAO()
    cliente_dao = ClienteDAO()
    venta_dao = VentaDAO()

    # ---------- COLORES ----------

    COLOR_DORADO = "#DDA400"
    COLOR_ROJO = "#F44336"
    COLOR_VERDE = "#39A844"

    # Color oscuro para los títulos
    COLOR_TITULO = "#212121"

    # Color claro únicamente para bordes
    COLOR_BORDE = "#E5E7EB"

    COLOR_TEXTO = "#666666"
    COLOR_FONDO = "#F7F7F7"

    # ---------- DATOS ----------

    productos = []
    clientes = []

    productos_por_id = {}
    clientes_por_id = {}

    # Productos agregados antes de registrar la venta
    detalles_temporales = []

    # ---------- MENSAJE ----------

    mensaje = ft.Text(
        value="",
        size=15
    )

    # ---------- CAMPOS ----------

    producto_dropdown = ft.Dropdown(
        label="Producto",
        hint_text="Selecciona un producto",
        width=525,
        options=[]
    )

    cantidad_input = ft.TextField(
        label="Cantidad",
        value="1",
        width=210,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    cliente_dropdown = ft.Dropdown(
        label="Cliente",
        hint_text="Selecciona un cliente",
        width=475,
        options=[]
    )

    metodo_pago_dropdown = ft.Dropdown(
        label="Método de pago",
        value="Efectivo",
        width=325,
        options=[
            ft.DropdownOption(
                key="Efectivo",
                text="Efectivo"
            ),
            ft.DropdownOption(
                key="Tarjeta",
                text="Tarjeta"
            ),
            ft.DropdownOption(
                key="Transferencia",
                text="Transferencia"
            )
        ]
    )

    estado_dropdown = ft.Dropdown(
        label="Estado",
        value="Pagada",
        width=275,
        options=[
            ft.DropdownOption(
                key="Pagada",
                text="Pagada"
            ),
            ft.DropdownOption(
                key="Pendiente",
                text="Pendiente"
            )
        ]
    )

    # ---------- TOTALES ----------

    subtotal_texto = ft.Text(
        "Subtotal: $0.00",
        size=16,
        color=COLOR_TITULO,
        weight=ft.FontWeight.BOLD
    )

    iva_texto = ft.Text(
        "IVA: $0.00",
        size=16,
        color=COLOR_TITULO
    )

    total_texto = ft.Text(
        "Total: $0.00",
        size=20,
        color=COLOR_DORADO,
        weight=ft.FontWeight.BOLD
    )

    # ---------- TABLA DEL CARRITO ----------

    carrito_tabla = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    "Producto",
                    color=COLOR_TITULO,
                    weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Precio",
                    color=COLOR_TITULO,
                    weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Cantidad",
                    color=COLOR_TITULO,
                    weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Subtotal",
                    color=COLOR_TITULO,
                    weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Acción",
                    color=COLOR_TITULO,
                    weight=ft.FontWeight.BOLD
                )
            )
        ],
        rows=[]
    )

    # ---------- TABLA DE VENTAS ----------

    ventas_tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("IVA")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Pago")),
            ft.DataColumn(ft.Text("Estado"))
        ],
        rows=[]
    )

    # ---------- FUNCIONES AUXILIARES ----------

    def mostrar_mensaje(texto, color):

        mensaje.value = texto
        mensaje.color = color

    def obtener_subtotal_carrito():

        subtotal = Decimal("0.00")

        for detalle in detalles_temporales:
            subtotal += Decimal(str(detalle.subtotal))

        return subtotal

    def actualizar_totales():

        subtotal = obtener_subtotal_carrito()
        iva = subtotal * Decimal("0.16")
        total = subtotal + iva

        subtotal_texto.value = (
            f"Subtotal: ${subtotal:.2f}"
        )

        iva_texto.value = (
            f"IVA: ${iva:.2f}"
        )

        total_texto.value = (
            f"Total: ${total:.2f}"
        )

    # ---------- CARGAR PRODUCTOS ----------

    def cargar_productos():

        nonlocal productos
        nonlocal productos_por_id

        productos = producto_dao.obtener_productos()

        productos_por_id = {
            producto.id_producto: producto
            for producto in productos
        }

        producto_dropdown.options.clear()

        for producto in productos:

            texto_producto = (
                f"{producto.nombre} | "
                f"{producto.marca} | "
                f"Talla: {producto.talla} | "
                f"Stock: {producto.stock_actual} | "
                f"${Decimal(str(producto.precio)):.2f}"
            )

            producto_dropdown.options.append(
                ft.DropdownOption(
                    key=str(producto.id_producto),
                    text=texto_producto
                )
            )

    # ---------- CARGAR CLIENTES ----------

    def cargar_clientes():

        nonlocal clientes
        nonlocal clientes_por_id

        clientes = cliente_dao.obtener_clientes()

        clientes_por_id = {
            cliente.id_cliente: cliente
            for cliente in clientes
        }

        cliente_dropdown.options.clear()

        for cliente in clientes:

            cliente_dropdown.options.append(
                ft.DropdownOption(
                    key=str(cliente.id_cliente),
                    text=(
                        f"{cliente.nombre} - "
                        f"{cliente.telefono}"
                    )
                )
            )

    # ---------- ELIMINAR DEL CARRITO ----------

    def eliminar_del_carrito(id_producto, page):

        detalle_a_eliminar = None

        for detalle in detalles_temporales:

            if detalle.id_producto == id_producto:
                detalle_a_eliminar = detalle
                break

        if detalle_a_eliminar is not None:
            detalles_temporales.remove(
                detalle_a_eliminar
            )

        cargar_tabla_carrito()
        actualizar_totales()

        mostrar_mensaje(
            "Producto eliminado de la venta.",
            COLOR_ROJO
        )

        page.update()

    # ---------- CARGAR CARRITO ----------

    def cargar_tabla_carrito():

        carrito_tabla.rows.clear()

        for detalle in detalles_temporales:

            producto = productos_por_id.get(
                detalle.id_producto
            )

            if producto is None:
                continue

            precio = Decimal(
                str(producto.precio)
            )

            carrito_tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                producto.nombre,
                                color=COLOR_TITULO
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                f"${precio:.2f}",
                                color=COLOR_TITULO
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                str(detalle.cantidad),
                                color=COLOR_TITULO
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                f"${detalle.subtotal:.2f}",
                                color=COLOR_TITULO
                            )
                        ),

                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=COLOR_ROJO,
                                tooltip="Quitar producto",
                                on_click=lambda e,
                                id_producto=detalle.id_producto:
                                eliminar_del_carrito(
                                    id_producto,
                                    e.page
                                )
                            )
                        )
                    ]
                )
            )

    # ---------- AGREGAR PRODUCTO ----------

    def agregar_producto(e):

        mostrar_mensaje("", COLOR_VERDE)

        if not producto_dropdown.value:

            mostrar_mensaje(
                "Selecciona un producto.",
                COLOR_ROJO
            )

            e.page.update()
            return

        if not cantidad_input.value:

            mostrar_mensaje(
                "Escribe la cantidad.",
                COLOR_ROJO
            )

            e.page.update()
            return

        try:
            id_producto = int(
                producto_dropdown.value
            )

            cantidad = int(
                cantidad_input.value
            )

        except ValueError:

            mostrar_mensaje(
                "La cantidad debe ser un número entero.",
                COLOR_ROJO
            )

            e.page.update()
            return

        if cantidad <= 0:

            mostrar_mensaje(
                "La cantidad debe ser mayor que cero.",
                COLOR_ROJO
            )

            e.page.update()
            return

        producto = productos_por_id.get(
            id_producto
        )

        if producto is None:

            mostrar_mensaje(
                "No se encontró el producto.",
                COLOR_ROJO
            )

            e.page.update()
            return

        detalle_existente = None
        cantidad_actual = 0

        for detalle in detalles_temporales:

            if detalle.id_producto == id_producto:

                detalle_existente = detalle
                cantidad_actual = detalle.cantidad
                break

        nueva_cantidad = (
            cantidad_actual + cantidad
        )

        if nueva_cantidad > producto.stock_actual:

            mostrar_mensaje(
                (
                    "Stock insuficiente. "
                    f"Solo hay "
                    f"{producto.stock_actual} "
                    "unidades disponibles."
                ),
                COLOR_ROJO
            )

            e.page.update()
            return

        precio = Decimal(
            str(producto.precio)
        )

        if detalle_existente is not None:

            detalle_existente.cantidad = (
                nueva_cantidad
            )

            detalle_existente.subtotal = (
                precio *
                Decimal(nueva_cantidad)
            )

        else:

            nuevo_detalle = DetalleVenta(
                id_detalle=None,
                id_venta=None,
                id_producto=id_producto,
                cantidad=cantidad,
                subtotal=(
                    precio *
                    Decimal(cantidad)
                )
            )

            detalles_temporales.append(
                nuevo_detalle
            )

        producto_dropdown.value = None
        cantidad_input.value = "1"

        cargar_tabla_carrito()
        actualizar_totales()

        mostrar_mensaje(
            (
                f"Producto '{producto.nombre}' "
                "agregado a la venta."
            ),
            COLOR_VERDE
        )

        e.page.update()

    # ---------- CARGAR VENTAS ----------

    def cargar_ventas():

        ventas_tabla.rows.clear()

        ventas = venta_dao.obtener_ventas()

        for venta in ventas:

            cliente = clientes_por_id.get(
                venta.id_cliente
            )

            if cliente is not None:
                nombre_cliente = cliente.nombre
            else:
                nombre_cliente = (
                    f"Cliente #{venta.id_cliente}"
                )

            if venta.estado == "Pagada":
                color_estado = COLOR_VERDE
            else:
                color_estado = COLOR_DORADO

            ventas_tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(venta.id_venta)
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                str(venta.fecha_venta)
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                str(venta.id_usuario)
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                nombre_cliente
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                (
                                    f"${Decimal(str(venta.iva)):.2f}"
                                )
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                (
                                    f"${Decimal(str(venta.total)):.2f}"
                                )
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                venta.metodo_pago
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                venta.estado,
                                color=color_estado,
                                weight=ft.FontWeight.BOLD
                            )
                        )
                    ]
                )
            )

    # ---------- REGISTRAR VENTA ----------

    def registrar_venta(e):

        mostrar_mensaje("", COLOR_VERDE)

        if not cliente_dropdown.value:

            mostrar_mensaje(
                "Selecciona un cliente.",
                COLOR_ROJO
            )

            e.page.update()
            return

        if len(detalles_temporales) == 0:

            mostrar_mensaje(
                (
                    "Agrega por lo menos "
                    "un producto."
                ),
                COLOR_ROJO
            )

            e.page.update()
            return

        if not metodo_pago_dropdown.value:

            mostrar_mensaje(
                (
                    "Selecciona el método "
                    "de pago."
                ),
                COLOR_ROJO
            )

            e.page.update()
            return

        if not estado_dropdown.value:

            mostrar_mensaje(
                (
                    "Selecciona el estado "
                    "de la venta."
                ),
                COLOR_ROJO
            )

            e.page.update()
            return

        try:
            id_cliente = int(
                cliente_dropdown.value
            )

            subtotal = obtener_subtotal_carrito()
            iva = subtotal * Decimal("0.16")
            total = subtotal + iva

            nueva_venta = Venta(
                id_venta=None,
                id_usuario=(
                    usuario_actual.id_usuario
                ),
                id_cliente=id_cliente,
                fecha_venta=date.today(),
                metodo_pago=(
                    metodo_pago_dropdown.value
                ),
                iva=iva,
                total=total,
                estado=estado_dropdown.value
            )

            id_venta = (
                venta_dao.registrar_venta(
                    nueva_venta,
                    detalles_temporales
                )
            )

            if not id_venta:

                mostrar_mensaje(
                    (
                        "No fue posible "
                        "registrar la venta."
                    ),
                    COLOR_ROJO
                )

                e.page.update()
                return

            detalles_temporales.clear()

            cliente_dropdown.value = None
            producto_dropdown.value = None
            cantidad_input.value = "1"

            metodo_pago_dropdown.value = (
                "Efectivo"
            )

            estado_dropdown.value = (
                "Pagada"
            )

            cargar_tabla_carrito()
            actualizar_totales()

            # Recarga los productos porque cambió el stock
            cargar_productos()
            cargar_ventas()

            mostrar_mensaje(
                (
                    f"Venta #{id_venta} "
                    "registrada correctamente."
                ),
                COLOR_VERDE
            )

        except (ValueError, InvalidOperation):

            mostrar_mensaje(
                (
                    "Existe un dato "
                    "numérico incorrecto."
                ),
                COLOR_ROJO
            )

        except Exception as error:

            mostrar_mensaje(
                (
                    "Error al registrar "
                    f"la venta: {error}"
                ),
                COLOR_ROJO
            )

        e.page.update()

    # ---------- CARGA INICIAL ----------

    cargar_productos()
    cargar_clientes()
    cargar_ventas()
    actualizar_totales()

    # ---------- INTERFAZ ----------

    return ft.Container(
        expand=True,
        padding=35,
        bgcolor=COLOR_FONDO,
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Ventas",
                                    size=30,
                                    weight=(
                                        ft.FontWeight.BOLD
                                    ),
                                    color=COLOR_TITULO
                                ),

                                ft.Text(
                                    (
                                        "Registro de ventas "
                                        "con varios productos"
                                    ),
                                    size=16,
                                    color=COLOR_TEXTO
                                ),

                                ft.Text(
                                    (
                                        "Usuario: "
                                        f"{usuario_actual.nombre}"
                                    ),
                                    size=15,
                                    color=COLOR_DORADO,
                                    weight=(
                                        ft.FontWeight.BOLD
                                    )
                                ),

                                ft.Container(
                                    width=115,
                                    height=4,
                                    bgcolor=COLOR_ROJO
                                )
                            ],
                            spacing=10
                        ),

                        ft.OutlinedButton(
                            "Regresar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: regresar()
                        )
                    ],
                    alignment=(
                        ft.MainAxisAlignment
                        .SPACE_BETWEEN
                    )
                ),

                # Formulario
                ft.Container(
                    padding=30,
                    border=ft.Border.all(
                        1,
                        COLOR_BORDE
                    ),
                    border_radius=14,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Registrar nueva venta",
                                size=24,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                                color=COLOR_TITULO
                            ),

                            ft.Text(
                                "1. Agrega los productos",
                                size=18,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                                color=COLOR_TITULO
                            ),

                            ft.Row(
                                controls=[
                                    producto_dropdown,
                                    cantidad_input,

                                    ft.ElevatedButton(
                                        "Agregar producto",
                                        icon=(
                                            ft.Icons
                                            .ADD_SHOPPING_CART
                                        ),
                                        bgcolor=COLOR_DORADO,
                                        color=ft.Colors.BLACK,
                                        on_click=(
                                            agregar_producto
                                        )
                                    )
                                ],
                                wrap=True
                            ),

                            ft.Divider(),

                            ft.Text(
                                "Productos de la venta",
                                size=18,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                                color=COLOR_TITULO
                            ),

                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        carrito_tabla
                                    ],
                                    scroll=(
                                        ft.ScrollMode.AUTO
                                    )
                                ),
                                border=ft.Border.all(
                                    1,
                                    COLOR_BORDE
                                ),
                                border_radius=10,
                                padding=10
                            ),

                            ft.Row(
                                controls=[
                                    subtotal_texto,
                                    iva_texto,
                                    total_texto
                                ],
                                spacing=30,
                                wrap=True
                            ),

                            ft.Divider(),

                            ft.Text(
                                (
                                    "2. Datos generales "
                                    "de la venta"
                                ),
                                size=18,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                                color=COLOR_TITULO
                            ),

                            ft.Row(
                                controls=[
                                    cliente_dropdown,
                                    metodo_pago_dropdown,
                                    estado_dropdown,

                                    ft.ElevatedButton(
                                        "Registrar venta",
                                        icon=(
                                            ft.Icons
                                            .POINT_OF_SALE
                                        ),
                                        bgcolor=COLOR_DORADO,
                                        color=ft.Colors.BLACK,
                                        on_click=(
                                            registrar_venta
                                        )
                                    )
                                ],
                                wrap=True
                            ),

                            mensaje
                        ],
                        spacing=18
                    )
                ),

                ft.Divider(),

                # Título de ventas registradas
                ft.Text(
                    "Ventas registradas",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TITULO
                ),

                # Tabla
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ventas_tabla
                        ],
                        scroll=ft.ScrollMode.AUTO
                    ),
                    border=ft.Border.all(
                        1,
                        COLOR_BORDE
                    ),
                    border_radius=12,
                    padding=15,
                    bgcolor=ft.Colors.WHITE
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )
    )