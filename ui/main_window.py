import flet as ft

from ui.categorias_view import categorias_view
from ui.clientes_view import clientes_view
from ui.facturas_view import facturas_view
from ui.inicio_view import inicio_view
from ui.login_view import login_view
from ui.producto_form import producto_form
from ui.productos_list import productos_list
from ui.usuarios_view import usuarios_view
from ui.ventas_view import ventas_view


def main_window(page: ft.Page):

    page.title = "Shecsper - Sistema de Inventario"
    page.window.width = 1200
    page.window.height = 720
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_100

    usuario_activo = {
        "usuario": None
    }

    contenido = ft.Container(
        padding=30,
        expand=True
    )

    def inicio():

        usuario = usuario_activo["usuario"]

        return inicio_view(usuario)

    def mostrar_inicio(e=None):

        contenido.content = inicio()
        page.update()

    def mostrar_productos(e=None):

        contenido.content = productos_list(
            mostrar_inicio,
            mostrar_formulario_producto,
            mostrar_formulario_producto
        )

        page.update()

    def mostrar_formulario_producto(producto=None):

        contenido.content = producto_form(
            mostrar_productos,
            producto
        )

        page.update()

    def mostrar_categorias(e=None):

        contenido.content = categorias_view(
            mostrar_inicio
        )

        page.update()

    def mostrar_clientes(e=None):

        contenido.content = clientes_view(
            mostrar_inicio
        )

        page.update()

    def mostrar_ventas(e=None):

        contenido.content = ventas_view(
            mostrar_inicio,
            usuario_activo["usuario"]
        )

        page.update()

    def mostrar_facturas(e=None):

        contenido.content = facturas_view(
            mostrar_inicio
        )

        page.update()

    def mostrar_usuarios(e=None):

        usuario = usuario_activo["usuario"]

        if usuario.rol.lower() != "administrador":

            mostrar_mensaje(
                "Acceso restringido",
                "Solo el administrador puede "
                "gestionar usuarios."
            )

            return

        contenido.content = usuarios_view(
            mostrar_inicio
        )

        page.update()

    def mostrar_mensaje(titulo, texto):

        contenido.content = ft.Column(
            controls=[
                ft.Text(
                    titulo,
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Container(
                    width=70,
                    height=4,
                    bgcolor="#E74C3C"
                ),

                ft.Icon(
                    ft.Icons.LOCK,
                    size=70,
                    color="#D4A017"
                ),

                ft.Text(
                    texto,
                    size=16
                ),

                ft.OutlinedButton(
                    content=ft.Text("Regresar"),
                    icon=ft.Icons.ARROW_BACK,
                    on_click=mostrar_inicio
                )
            ],
            spacing=20
        )

        page.update()

    def boton_menu(texto, icono, funcion):

        return ft.ElevatedButton(
            content=ft.Text(texto),
            icon=icono,
            width=190,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            on_click=funcion
        )

    def cerrar_sesion(e=None):

        usuario_activo["usuario"] = None

        mostrar_login()

    def construir_sistema():

        usuario = usuario_activo["usuario"]

        opciones_menu = [
            boton_menu(
                "Inicio",
                ft.Icons.HOME,
                mostrar_inicio
            ),

            boton_menu(
                "Productos",
                ft.Icons.INVENTORY_2,
                mostrar_productos
            ),

            boton_menu(
                "Categorías",
                ft.Icons.CATEGORY,
                mostrar_categorias
            ),

            boton_menu(
                "Clientes",
                ft.Icons.PEOPLE,
                mostrar_clientes
            ),

            boton_menu(
                "Ventas",
                ft.Icons.POINT_OF_SALE,
                mostrar_ventas
            ),

            boton_menu(
                "Facturas",
                ft.Icons.RECEIPT_LONG,
                mostrar_facturas
            )
        ]

        if usuario.rol.lower() == "administrador":

            opciones_menu.append(
                boton_menu(
                    "Usuarios",
                    ft.Icons.MANAGE_ACCOUNTS,
                    mostrar_usuarios
                )
            )

        menu_lateral = ft.Container(
            width=230,
            bgcolor=ft.Colors.BLACK,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "SHECSPER",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),

                    ft.Text(
                        "SISTEMA DE INVENTARIO",
                        size=12,
                        color="#D4A017"
                    ),

                    ft.Divider(
                        color=ft.Colors.GREY_800
                    ),

                    *opciones_menu,

                    ft.Container(
                        expand=True
                    ),

                    ft.Divider(
                        color=ft.Colors.GREY_800
                    ),

                    ft.Text(
                        usuario.nombre,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        usuario.rol.upper(),
                        color="#D4A017",
                        size=12
                    ),

                    ft.TextButton(
                        content=ft.Text("Cerrar sesión"),
                        icon=ft.Icons.LOGOUT,
                        style=ft.ButtonStyle(
                            color=ft.Colors.RED
                        ),
                        on_click=cerrar_sesion
                    )
                ],
                spacing=12,
                expand=True
            )
        )

        layout = ft.Row(
            controls=[
                menu_lateral,
                contenido
            ],
            expand=True,
            spacing=0
        )

        page.clean()
        page.add(layout)

        mostrar_inicio()

    def iniciar_sesion(usuario):

        usuario_activo["usuario"] = usuario

        construir_sistema()

    def mostrar_login():

        page.clean()

        page.add(
            login_view(
                iniciar_sesion
            )
        )

        page.update()

    mostrar_login()