import flet as ft

from dao.cliente_dao import ClienteDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from models.venta import Venta


def ventas_view(regresar, usuario_activo):

    producto_input = ft.Dropdown(
        label="Producto",
        width=340
    )

    cliente_input = ft.Dropdown(
        label="Cliente",
        width=300
    )

    cantidad_input = ft.TextField(
        label="Cantidad",
        width=150,
        value="1"
    )

    metodo_pago_input = ft.Dropdown(
        label="Método de pago",
        width=220,
        value="Efectivo",
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

    estado_input = ft.Dropdown(
        label="Estado",
        width=180,
        value="Pagada",
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

    mensaje = ft.Text("")

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Pago")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[]
    )

    def formato_moneda(valor):

        if valor is None:
            return "-"

        return f"${valor:.2f}"

    def cargar_catalogos():

        productos = ProductoDAO().obtener_productos()
        clientes = ClienteDAO().obtener_clientes()

        producto_input.options = []

        for producto in productos:

            producto_input.options.append(
                ft.DropdownOption(
                    key=str(producto.id_producto),
                    text=(
                        f"{producto.nombre} - "
                        f"Talla: {producto.talla} - "
                        f"Stock: {producto.stock_actual}"
                    )
                )
            )

        cliente_input.options = []

        for cliente in clientes:

            cliente_input.options.append(
                ft.DropdownOption(
                    key=str(cliente.id_cliente),
                    text=cliente.nombre
                )
            )

    def cargar_ventas():

        try:
            ventas = VentaDAO().obtener_ventas()

            tabla.rows.clear()

            for venta in ventas:

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(str(venta[0]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[1]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[2]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[3]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[4]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[5]))
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(venta[6])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(venta[7])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[8]))
                            ),

                            ft.DataCell(
                                ft.Text(str(venta[9]))
                            ),
                        ]
                    )
                )

            if len(ventas) == 0:
                mensaje.value = "No hay ventas registradas"
                mensaje.color = ft.Colors.RED
            else:
                mensaje.value = (
                    f"Ventas encontradas: {len(ventas)}"
                )
                mensaje.color = ft.Colors.GREEN

        except Exception as error:
            mensaje.value = (
                f"Error al consultar ventas: {error}"
            )
            mensaje.color = ft.Colors.RED

    def registrar_venta(e):

        if (
            producto_input.value is None
            or cliente_input.value is None
            or cantidad_input.value == ""
            or metodo_pago_input.value is None
            or estado_input.value is None
        ):
            mensaje.value = (
                "Completa todos los datos de la venta"
            )
            mensaje.color = ft.Colors.RED
            e.control.page.update()
            return

        try:
            cantidad = int(cantidad_input.value)

            nueva_venta = Venta(
                id_usuario=usuario_activo.id_usuario,
                id_cliente=int(cliente_input.value),
                id_producto=int(producto_input.value),
                metodo_pago=metodo_pago_input.value,
                cantidad=cantidad,
                estado=estado_input.value
            )

            id_venta = VentaDAO().registrar(
                nueva_venta
            )

            mensaje.value = (
                f"Venta número {id_venta} "
                "registrada correctamente"
            )
            mensaje.color = ft.Colors.GREEN

            producto_input.value = None
            cliente_input.value = None
            cantidad_input.value = "1"
            metodo_pago_input.value = "Efectivo"
            estado_input.value = "Pagada"

            cargar_catalogos()
            cargar_ventas()

        except ValueError as error:
            mensaje.value = str(error)
            mensaje.color = ft.Colors.RED

        except Exception as error:
            mensaje.value = (
                f"No se pudo registrar la venta: {error}"
            )
            mensaje.color = ft.Colors.RED

        e.control.page.update()

    cargar_catalogos()
    cargar_ventas()

    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Ventas",
                                    size=27,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Registro de ventas y "
                                    "actualización de existencias",
                                    color=ft.Colors.GREY_700
                                ),

                                ft.Text(
                                    f"Usuario: {usuario_activo.nombre}",
                                    color="#D4A017",
                                    weight=ft.FontWeight.BOLD
                                ),
                            ]
                        ),

                        ft.OutlinedButton(
                            content=ft.Text("Regresar"),
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: regresar()
                        )
                    ],
                    alignment=(
                        ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),

                ft.Container(
                    width=70,
                    height=4,
                    bgcolor="#E74C3C"
                ),

                ft.Container(
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    border=ft.Border.all(
                        1,
                        ft.Colors.GREY_300
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Registrar nueva venta",
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Row(
                                controls=[
                                    producto_input,
                                    cliente_input,
                                    cantidad_input
                                ],
                                wrap=True
                            ),

                            ft.Row(
                                controls=[
                                    metodo_pago_input,
                                    estado_input,

                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "Registrar venta"
                                        ),
                                        icon=ft.Icons.POINT_OF_SALE,
                                        bgcolor="#D4A017",
                                        color=ft.Colors.BLACK,
                                        on_click=registrar_venta
                                    )
                                ],
                                wrap=True
                            )
                        ]
                    )
                ),

                ft.Divider(),

                ft.Row(
                    controls=[tabla],
                    scroll=ft.ScrollMode.AUTO
                ),

                mensaje
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )
    )