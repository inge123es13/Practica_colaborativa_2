import flet as ft

from decimal import Decimal

from dao.factura_dao import FacturaDAO
from utils.factura_pdf import generar_factura_pdf


def facturas_view(regresar):

    COLOR_DORADO = "#D4A017"
    COLOR_ROJO = "#E74C3C"
    COLOR_TITULO = "#212121"
    COLOR_BORDE = "#E5E7EB"

    mensaje = ft.Text("")

    # ---------- TABLA ----------

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Folio")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Venta")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Productos")),
            ft.DataColumn(ft.Text("Subtotal")),
            ft.DataColumn(ft.Text("IVA")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Pago")),
            ft.DataColumn(ft.Text("Estado")),

            # Nueva columna
            ft.DataColumn(ft.Text("PDF"))
        ],
        rows=[]
    )

    # ---------- FORMATO MONEDA ----------

    def formato_moneda(valor):

        if valor is None:
            return "$0.00"

        numero = Decimal(str(valor))

        return f"${numero:.2f}"

    # ---------- GENERAR PDF ----------

    def crear_pdf(id_factura, e):

        try:
            factura_dao = FacturaDAO()

            factura, detalles = (
                factura_dao.obtener_factura_completa(
                    id_factura
                )
            )

            if factura is None:

                mensaje.value = (
                    "No fue posible encontrar "
                    "la factura."
                )

                mensaje.color = ft.Colors.RED
                e.page.update()
                return

            ruta = generar_factura_pdf(
                factura,
                detalles
            )

            mensaje.value = (
                "Factura generada correctamente: "
                f"{ruta}"
            )

            mensaje.color = ft.Colors.GREEN

        except Exception as error:

            mensaje.value = (
                "Error al generar el PDF: "
                f"{error}"
            )

            mensaje.color = ft.Colors.RED

        e.page.update()

    # ---------- CARGAR FACTURAS ----------

    def cargar_facturas():

        try:
            factura_dao = FacturaDAO()

            generadas = (
                factura_dao
                .generar_facturas_faltantes()
            )

            facturas = (
                factura_dao.obtener_facturas()
            )

            tabla.rows.clear()

            for factura in facturas:

                estado = str(factura[9])

                if estado == "Emitida":
                    color_fondo = (
                        ft.Colors.GREEN_100
                    )

                    color_texto = (
                        ft.Colors.GREEN_900
                    )

                elif estado == "Pendiente":
                    color_fondo = (
                        ft.Colors.AMBER_100
                    )

                    color_texto = (
                        ft.Colors.AMBER_900
                    )

                else:
                    color_fondo = (
                        ft.Colors.GREY_200
                    )

                    color_texto = (
                        ft.Colors.GREY_900
                    )

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(factura[0])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(factura[1])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(factura[2])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    (
                                        f"Venta "
                                        f"#{factura[3]}"
                                    )
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(factura[4])
                                )
                            ),

                            ft.DataCell(
                                ft.Container(
                                    width=230,
                                    content=ft.Text(
                                        str(factura[10]),
                                        max_lines=3,
                                        overflow=(
                                            ft.TextOverflow
                                            .ELLIPSIS
                                        )
                                    )
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(
                                        factura[5]
                                    )
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(
                                        factura[6]
                                    )
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    formato_moneda(
                                        factura[7]
                                    ),
                                    weight=(
                                        ft.FontWeight.BOLD
                                    ),
                                    color=COLOR_DORADO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(factura[8])
                                )
                            ),

                            ft.DataCell(
                                ft.Container(
                                    padding=8,
                                    border_radius=8,
                                    bgcolor=color_fondo,
                                    content=ft.Text(
                                        estado,
                                        color=color_texto
                                    )
                                )
                            ),

                            # Botón PDF de cada factura
                            ft.DataCell(
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "Generar"
                                    ),
                                    icon=(
                                        ft.Icons
                                        .PICTURE_AS_PDF
                                    ),
                                    bgcolor=COLOR_ROJO,
                                    color=ft.Colors.WHITE,
                                    on_click=lambda e,
                                    id_factura=factura[0]:
                                    crear_pdf(
                                        id_factura,
                                        e
                                    )
                                )
                            )
                        ]
                    )
                )

            if generadas > 0:

                mensaje.value = (
                    f"Se generaron {generadas} "
                    "facturas faltantes."
                )

                mensaje.color = ft.Colors.GREEN

            elif len(facturas) == 0:

                mensaje.value = (
                    "No hay facturas registradas."
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
                "Error al consultar facturas: "
                f"{error}"
            )

            mensaje.color = ft.Colors.RED

    # ---------- CARGA INICIAL ----------

    cargar_facturas()

    # ---------- INTERFAZ ----------

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
                                    weight=(
                                        ft.FontWeight.BOLD
                                    ),
                                    color=COLOR_TITULO
                                ),

                                ft.Text(
                                    (
                                        "Consulta y genera "
                                        "las facturas en PDF"
                                    ),
                                    color=ft.Colors.GREY_700
                                )
                            ]
                        ),

                        ft.OutlinedButton(
                            content=ft.Text(
                                "Regresar"
                            ),
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: regresar()
                        )
                    ],
                    alignment=(
                        ft.MainAxisAlignment
                        .SPACE_BETWEEN
                    )
                ),

                ft.Container(
                    width=70,
                    height=4,
                    bgcolor=COLOR_ROJO
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
                                color=COLOR_DORADO
                            ),

                            ft.Column(
                                controls=[
                                    ft.Text(
                                        (
                                            "FACTURACIÓN "
                                            "SHECSPER"
                                        ),
                                        size=20,
                                        weight=(
                                            ft.FontWeight.BOLD
                                        ),
                                        color=ft.Colors.WHITE
                                    ),

                                    ft.Text(
                                        (
                                            "Genera comprobantes "
                                            "PDF con datos del "
                                            "cliente y productos"
                                        ),
                                        color=ft.Colors.GREY_400
                                    )
                                ]
                            )
                        ]
                    )
                ),

                ft.Divider(),

                ft.Container(
                    padding=10,
                    border=ft.Border.all(
                        1,
                        COLOR_BORDE
                    ),
                    border_radius=12,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Row(
                        controls=[tabla],
                        scroll=ft.ScrollMode.AUTO
                    )
                ),

                mensaje
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )
    )