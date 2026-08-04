import flet as ft

from dao.cliente_dao import ClienteDAO
from models.cliente import Cliente


def clientes_view(regresar):

    cliente_seleccionado = {
        "id": 0
    }

    nombre_input = ft.TextField(
        label="Nombre completo",
        width=300
    )

    telefono_input = ft.TextField(
        label="Teléfono",
        width=200
    )

    correo_input = ft.TextField(
        label="Correo electrónico",
        width=300
    )

    direccion_input = ft.TextField(
        label="Dirección",
        width=400
    )

    mensaje = ft.Text("")

    titulo_formulario = ft.Text(
        "Registrar cliente",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    texto_boton = ft.Text(
        "Guardar cliente"
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def limpiar_formulario():

        cliente_seleccionado["id"] = 0

        nombre_input.value = ""
        telefono_input.value = ""
        correo_input.value = ""
        direccion_input.value = ""

        titulo_formulario.value = "Registrar cliente"
        texto_boton.value = "Guardar cliente"

    def seleccionar_cliente(cliente):

        cliente_seleccionado["id"] = (
            cliente.id_cliente
        )

        nombre_input.value = cliente.nombre
        telefono_input.value = cliente.telefono
        correo_input.value = cliente.correo
        direccion_input.value = cliente.direccion

        titulo_formulario.value = "Editar cliente"
        texto_boton.value = "Actualizar cliente"

        nombre_input.update()
        telefono_input.update()
        correo_input.update()
        direccion_input.update()
        titulo_formulario.update()
        texto_boton.update()

    def cargar_clientes():

        try:
            cliente_dao = ClienteDAO()
            clientes = cliente_dao.obtener_clientes()

            tabla.rows.clear()

            for cliente in clientes:

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(cliente.id_cliente)
                                )
                            ),

                            ft.DataCell(
                                ft.Text(cliente.nombre)
                            ),

                            ft.DataCell(
                                ft.Text(cliente.telefono)
                            ),

                            ft.DataCell(
                                ft.Text(cliente.correo)
                            ),

                            ft.DataCell(
                                ft.Text(cliente.direccion)
                            ),

                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="#D4A017",
                                            tooltip="Editar cliente",
                                            on_click=lambda e, c=cliente:
                                                seleccionar_cliente(c)
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            tooltip="Eliminar cliente",
                                            on_click=lambda e, c=cliente:
                                                confirmar_eliminacion(e, c)
                                        )
                                    ]
                                )
                            ),
                        ]
                    )
                )

            if len(clientes) == 0:
                mensaje.value = "No hay clientes registrados"
                mensaje.color = ft.Colors.RED
            else:
                mensaje.value = (
                    f"Clientes encontrados: {len(clientes)}"
                )
                mensaje.color = ft.Colors.GREEN

        except Exception as error:
            mensaje.value = (
                f"Error al consultar clientes: {error}"
            )
            mensaje.color = ft.Colors.RED

    def guardar_cliente(e):

        nombre = nombre_input.value
        telefono = telefono_input.value
        correo = correo_input.value
        direccion = direccion_input.value

        if (
            nombre == ""
            or telefono == ""
            or correo == ""
            or direccion == ""
        ):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            e.control.page.update()
            return

        cliente = Cliente(
            id_cliente=cliente_seleccionado["id"],
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            correo=correo
        )

        cliente_dao = ClienteDAO()

        if cliente_seleccionado["id"] == 0:

            resultado = cliente_dao.insertar(cliente)
            texto_exito = "Cliente registrado correctamente"

        else:

            resultado = cliente_dao.actualizar(cliente)
            texto_exito = "Cliente actualizado correctamente"

        if resultado:

            mensaje.value = texto_exito
            mensaje.color = ft.Colors.GREEN

            limpiar_formulario()
            cargar_clientes()

        else:
            mensaje.value = "No fue posible guardar el cliente"
            mensaje.color = ft.Colors.RED

        e.control.page.update()

    def confirmar_eliminacion(e, cliente):

        page = e.control.page

        def cancelar(e):
            page.pop_dialog()

        def eliminar(e):

            resultado = ClienteDAO().eliminar(
                cliente.id_cliente
            )

            page.pop_dialog()

            if resultado:
                mensaje.value = (
                    f"Cliente '{cliente.nombre}' "
                    "eliminado correctamente"
                )
                mensaje.color = ft.Colors.GREEN

                cargar_clientes()

            else:
                mensaje.value = (
                    "No se pudo eliminar el cliente. "
                    "Puede estar relacionado con una venta."
                )
                mensaje.color = ft.Colors.RED

            page.update()

        ventana = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar cliente"),
            content=ft.Text(
                f"¿Realmente deseas eliminar "
                f"'{cliente.nombre}'?"
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

    cargar_clientes()

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
                                    "Clientes",
                                    size=27,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Administración de clientes "
                                    "de Shecsper",
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
                                    telefono_input,
                                    correo_input
                                ],
                                wrap=True
                            ),

                            ft.Row(
                                controls=[
                                    direccion_input,

                                    ft.ElevatedButton(
                                        content=texto_boton,
                                        icon=ft.Icons.SAVE,
                                        bgcolor="#D4A017",
                                        color=ft.Colors.BLACK,
                                        on_click=guardar_cliente
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