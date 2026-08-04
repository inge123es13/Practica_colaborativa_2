import flet as ft

from dao.producto_dao import ProductoDAO


def inicio_view(usuario):

    resumen = ProductoDAO().obtener_resumen()

    def tarjeta(
        titulo,
        valor,
        icono,
        color
    ):

        return ft.Container(
            width=230,
            height=135,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300
            ),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=55,
                        height=55,
                        border_radius=30,
                        bgcolor=color,
                        content=ft.Icon(
                            icono,
                            size=30,
                            color=ft.Colors.WHITE
                        ),
                        alignment=ft.Alignment.CENTER
                    ),

                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                color=ft.Colors.GREY_700
                            ),

                            ft.Text(
                                str(valor),
                                size=30,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        spacing=4,
                        alignment=(
                            ft.MainAxisAlignment.CENTER
                        )
                    )
                ]
            )
        )

    return ft.Column(
        controls=[
            ft.Text(
                "Panel principal",
                size=30,
                weight=ft.FontWeight.BOLD
            ),

            ft.Container(
                width=80,
                height=4,
                bgcolor="#E74C3C"
            ),

            ft.Text(
                f"Bienvenido, {usuario.nombre}",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#D4A017"
            ),

            ft.Text(
                "Resumen general del inventario de Shecsper",
                color=ft.Colors.GREY_700
            ),

            ft.Row(
                controls=[
                    tarjeta(
                        "Productos",
                        resumen["productos"],
                        ft.Icons.INVENTORY_2,
                        ft.Colors.BLUE
                    ),

                    tarjeta(
                        "Existencias",
                        resumen["existencias"],
                        ft.Icons.WAREHOUSE,
                        ft.Colors.GREEN
                    ),

                    tarjeta(
                        "Stock bajo",
                        resumen["stock_bajo"],
                        ft.Icons.WARNING,
                        "#D4A017"
                    ),

                    tarjeta(
                        "Agotados",
                        resumen["agotados"],
                        ft.Icons.REMOVE_SHOPPING_CART,
                        ft.Colors.RED
                    )
                ],
                wrap=True,
                spacing=18
            ),

            ft.Container(
                margin=ft.Margin.only(top=15),
                padding=25,
                bgcolor=ft.Colors.BLACK,
                border_radius=12,
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.SPORTS_BASKETBALL,
                            size=55,
                            color="#D4A017"
                        ),

                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CONTROL INTERNO SHECSPER",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),

                                ft.Text(
                                    "Administra productos, categorías, "
                                    "clientes, ventas y facturas desde "
                                    "el menú lateral.",
                                    color=ft.Colors.GREY_400
                                )
                            ]
                        )
                    ]
                )
            )
        ],
        spacing=18,
        scroll=ft.ScrollMode.AUTO
    )