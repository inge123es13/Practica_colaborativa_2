import flet as ft

from dao.usuario_dao import UsuarioDAO


def login_view(iniciar_sesion):

    correo_input = ft.TextField(
        label="Correo electrónico",
        width=360,
        prefix_icon=ft.Icons.EMAIL
    )

    contrasena_input = ft.TextField(
        label="Contraseña",
        width=360,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK
    )

    mensaje = ft.Text("")

    def ingresar(e):

        correo = correo_input.value
        contrasena = contrasena_input.value

        if correo == "" or contrasena == "":

            mensaje.value = (
                "Escribe el correo y la contraseña"
            )
            mensaje.color = ft.Colors.RED

            e.control.page.update()
            return

        usuario_dao = UsuarioDAO()

        usuario = usuario_dao.autenticar(
            correo,
            contrasena
        )

        if usuario is None:

            mensaje.value = (
                "Correo o contraseña incorrectos"
            )
            mensaje.color = ft.Colors.RED

            e.control.page.update()
            return

        mensaje.value = ""
        iniciar_sesion(usuario)

    return ft.Row(
        controls=[
            ft.Container(
                expand=1,
                bgcolor=ft.Colors.BLACK,
                padding=50,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "SHECSPER",
                            size=48,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),

                        ft.Text(
                            "REPRESENTA TU ESENCIA",
                            size=18,
                            color="#D4A017"
                        ),

                        ft.Container(
                            width=100,
                            height=4,
                            bgcolor="#E74C3C"
                        ),

                        ft.Icon(
                            ft.Icons.INVENTORY_2,
                            size=120,
                            color="#D4A017"
                        ),

                        ft.Text(
                            "Sistema local para el control "
                            "del inventario",
                            size=17,
                            color=ft.Colors.WHITE
                        )
                    ],
                    spacing=18,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    )
                )
            ),

            ft.Container(
                expand=1,
                padding=60,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "INICIAR SESIÓN",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),

                        ft.Container(
                            width=80,
                            height=4,
                            bgcolor="#E74C3C"
                        ),

                        ft.Text(
                            "Accede al sistema de inventario",
                            size=16,
                            color=ft.Colors.GREY_700
                        ),

                        correo_input,
                        contrasena_input,

                        ft.ElevatedButton(
                            content=ft.Text("INGRESAR"),
                            icon=ft.Icons.LOGIN,
                            width=360,
                            height=50,
                            bgcolor="#D4A017",
                            color=ft.Colors.BLACK,
                            on_click=ingresar
                        ),

                        mensaje
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ],
        expand=True,
        spacing=0
    )