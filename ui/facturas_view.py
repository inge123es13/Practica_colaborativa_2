import flet as ft

from dao.factura_dao import FacturaDAO


def facturas_view(regresar):

    mensaje = ft.Text("")

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Folio")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Venta")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Subtotal")),
            ft.DataColumn(ft.Text("IVA")),
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

    def cargar_facturas():

        try:
            factura_dao = FacturaDAO()

            generadas = (
                factura_dao.generar_facturas_faltantes()
            )

            facturas = factura_dao.obtener_facturas()

            tabla.rows.clear()

            for factura in facturas:

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(str(factura[0]))
                            ),

                            ft.DataCell(
                                ft.Text(str(factura[1]))
                            ),

                            ft.DataCell(
                                ft.Text(str(factura[2]))
                            ),

                            ft.DataCell(
                                ft.Text(
                                    f"Venta #{factura[3]}"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(str(factura[4]))
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(factura[5])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(factura[6])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(factura[7]),
                                    weight=ft.FontWeight.BOLD,
                                    color="#D4A017"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(str(factura[8]))
                            ),

                            ft.DataCell(
                                ft.Container(
                                    padding=8,
                                    border_radius=8,
                                    bgcolor=ft.Colors.GREEN_100,
                                    content=ft.Text(
                                        str(factura[9]),
                                        color=ft.Colors.GREEN_900
                                    )
                                )
                            ),
                        ]
                    )
                )

            if generadas > 0:
                mensaje.value = (
                    f"Se generaron {generadas} "
                    "facturas faltantes"
                )
                mensaje.color = ft.Colors.GREEN

            elif len(facturas) == 0:
                mensaje.value = (
                    "No hay facturas registradas"
                )
                mensaje.color = ft.Colors.RED

            else:
                mensaje.value = (
                    f"Facturas encontradas: "
                    f"{len(facturas)}"
                )
                mensaje.color = ft.Colors.GREEN

        except Exception as error:
            mensaje.value = (
                f"Error al consultar facturas: {error}"
            )
            mensaje.color = ft.Colors.RED

    cargar_facturas()

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
                                    "Facturas",
                                    size=27,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Consulta las facturas "
                                    "generadas por las ventas",
                                    color=ft.Colors.GREY_700
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
                    bgcolor=ft.Colors.BLACK,
                    border_radius=12,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.RECEIPT_LONG,
                                size=45,
                                color="#D4A017"
                            ),

                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "FACTURACIÓN SHECSPER",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE
                                    ),

                                    ft.Text(
                                        "Las facturas se generan "
                                        "a partir de las ventas",
                                        color=ft.Colors.GREY_400
                                    )
                                ]
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