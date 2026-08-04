import flet as ft

from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario


def usuarios_view(regresar):

    usuario_seleccionado = {
        "id": 0
    }

    nombre_input = ft.TextField(
        label="Nombre completo",
        width=300
    )

    correo_input = ft.TextField(
        label="Correo electrónico",
        width=300
    )

    contrasena_input = ft.TextField(
        label="Contraseña",
        width=250,
        password=True,
        can_reveal_password=True
    )

    rol_input = ft.Dropdown(
        label="Rol",
        width=220,
        options=[
            ft.DropdownOption(
                key="administrador",
                text="Administrador"
            ),
            ft.DropdownOption(
                key="empleado",
                text="Empleado"
            )
        ]
    )

    mensaje = ft.Text("")

    titulo_formulario = ft.Text(
        "Registrar usuario",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    texto_boton = ft.Text(
        "Guardar usuario"
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Rol")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def limpiar_formulario():

        usuario_seleccionado["id"] = 0

        nombre_input.value = ""
        correo_input.value = ""
        contrasena_input.value = ""
        rol_input.value = None

        titulo_formulario.value = "Registrar usuario"
        texto_boton.value = "Guardar usuario"

    def seleccionar_usuario(usuario):

        usuario_seleccionado["id"] = (
            usuario.id_usuario
        )

        nombre_input.value = usuario.nombre
        correo_input.value = usuario.correo
        contrasena_input.value = usuario.contrasena
        rol_input.value = usuario.rol

        titulo_formulario.value = "Editar usuario"
        texto_boton.value = "Actualizar usuario"

        nombre_input.update()
        correo_input.update()
        contrasena_input.update()
        rol_input.update()
        titulo_formulario.update()
        texto_boton.update()

    def cargar_usuarios():

        try:
            usuario_dao = UsuarioDAO()
            usuarios = usuario_dao.obtener_usuarios()

            tabla.rows.clear()

            for usuario in usuarios:

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(usuario.id_usuario)
                                )
                            ),

                            ft.DataCell(
                                ft.Text(usuario.nombre)
                            ),

                            ft.DataCell(
                                ft.Text(usuario.correo)
                            ),

                            ft.DataCell(
                                ft.Container(
                                    padding=8,
                                    border_radius=8,
                                    bgcolor=(
                                        "#D4A017"
                                        if usuario.rol == "administrador"
                                        else ft.Colors.GREY_300
                                    ),
                                    content=ft.Text(
                                        usuario.rol.upper(),
                                        color=ft.Colors.BLACK
                                    )
                                )
                            ),

                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="#D4A017",
                                            tooltip="Editar usuario",
                                            on_click=lambda e, u=usuario:
                                                seleccionar_usuario(u)
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            tooltip="Eliminar usuario",
                                            on_click=lambda e, u=usuario:
                                                confirmar_eliminacion(e, u)
                                        )
                                    ]
                                )
                            ),
                        ]
                    )
                )

            if len(usuarios) == 0:
                mensaje.value = "No hay usuarios registrados"
                mensaje.color = ft.Colors.RED
            else:
                mensaje.value = (
                    f"Usuarios encontrados: {len(usuarios)}"
                )
                mensaje.color = ft.Colors.GREEN

        except Exception as error:
            mensaje.value = (
                f"Error al consultar usuarios: {error}"
            )
            mensaje.color = ft.Colors.RED

    def guardar_usuario(e):

        nombre = nombre_input.value
        correo = correo_input.value
        contrasena = contrasena_input.value
        rol = rol_input.value

        if (
            nombre == ""
            or correo == ""
            or contrasena == ""
            or rol is None
            or rol == ""
        ):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            e.control.page.update()
            return

        usuario = Usuario(
            id_usuario=usuario_seleccionado["id"],
            nombre=nombre,
            correo=correo,
            contrasena=contrasena,
            rol=rol
        )

        usuario_dao = UsuarioDAO()

        if usuario_seleccionado["id"] == 0:

            resultado = usuario_dao.insertar(usuario)
            texto_exito = "Usuario registrado correctamente"

        else:

            resultado = usuario_dao.actualizar(usuario)
            texto_exito = "Usuario actualizado correctamente"

        if resultado:

            mensaje.value = texto_exito
            mensaje.color = ft.Colors.GREEN

            limpiar_formulario()
            cargar_usuarios()

        else:
            mensaje.value = (
                "No fue posible guardar el usuario. "
                "Verifica que el correo no esté repetido."
            )
            mensaje.color = ft.Colors.RED

        e.control.page.update()

    def confirmar_eliminacion(e, usuario):

        page = e.control.page

        def cancelar(e):
            page.pop_dialog()

        def eliminar(e):

            resultado = UsuarioDAO().eliminar(
                usuario.id_usuario
            )

            page.pop_dialog()

            if resultado:
                mensaje.value = (
                    f"Usuario '{usuario.nombre}' "
                    "eliminado correctamente"
                )
                mensaje.color = ft.Colors.GREEN

                cargar_usuarios()

            else:
                mensaje.value = (
                    "No se pudo eliminar el usuario. "
                    "Puede estar relacionado con una venta."
                )
                mensaje.color = ft.Colors.RED

            page.update()

        ventana = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar usuario"),
            content=ft.Text(
                f"¿Realmente deseas eliminar "
                f"'{usuario.nombre}'?"
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cancelar"),
                    on_click=cancelar
                ),

                ft.ElevatedButton(
                    content=ft.Text("Eliminar"),
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=eliminar
                )
            ]
        )

        page.show_dialog(ventana)

    cargar_usuarios()

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
                                    "Usuarios",
                                    size=27,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Administradores y empleados "
                                    "del sistema",
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
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    border=ft.Border.all(
                        1,
                        ft.Colors.GREY_300
                    ),
                    content=ft.Column(
                        controls=[
                            titulo_formulario,

                            ft.Row(
                                controls=[
                                    nombre_input,
                                    correo_input,
                                    contrasena_input,
                                    rol_input
                                ],
                                wrap=True
                            ),

                            ft.ElevatedButton(
                                content=texto_boton,
                                icon=ft.Icons.SAVE,
                                bgcolor="#D4A017",
                                color=ft.Colors.BLACK,
                                on_click=guardar_usuario
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