import flet as ft

from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria


def categorias_view(regresar):

    categoria_seleccionada = {
        "id": 0
    }

    nombre_input = ft.TextField(
        label="Nombre de la categoría",
        width=300
    )

    descripcion_input = ft.TextField(
        label="Descripción",
        width=400
    )

    mensaje = ft.Text("")

    titulo_formulario = ft.Text(
        "Registrar categoría",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    texto_boton = ft.Text(
        "Guardar categoría"
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text("ID")
            ),
            ft.DataColumn(
                ft.Text("Categoría")
            ),
            ft.DataColumn(
                ft.Text("Descripción")
            ),
            ft.DataColumn(
                ft.Text("Acciones")
            ),
        ],
        rows=[]
    )

    def limpiar_formulario():

        categoria_seleccionada["id"] = 0

        nombre_input.value = ""
        descripcion_input.value = ""

        titulo_formulario.value = "Registrar categoría"
        texto_boton.value = "Guardar categoría"

    def seleccionar_categoria(categoria):

        categoria_seleccionada["id"] = (
            categoria.id_categoria
        )

        nombre_input.value = categoria.nombre
        descripcion_input.value = categoria.descripcion

        titulo_formulario.value = "Editar categoría"
        texto_boton.value = "Actualizar categoría"

        nombre_input.update()
        descripcion_input.update()
        titulo_formulario.update()
        texto_boton.update()

    def cargar_categorias():

        try:
            categoria_dao = CategoriaDAO()
            categorias = categoria_dao.obtener_categorias()

            tabla.rows.clear()

            for categoria in categorias:

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(categoria.id_categoria)
                                )
                            ),

                            ft.DataCell(
                                ft.Text(categoria.nombre)
                            ),

                            ft.DataCell(
                                ft.Text(categoria.descripcion)
                            ),

                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="#D4A017",
                                    tooltip="Editar categoría",
                                    on_click=lambda e, c=categoria:
                                        seleccionar_categoria(c)
                                )
                            ),
                        ]
                    )
                )

            if len(categorias) == 0:
                mensaje.value = (
                    "No hay categorías registradas"
                )
                mensaje.color = ft.Colors.RED
            else:
                mensaje.value = (
                    f"Categorías encontradas: "
                    f"{len(categorias)}"
                )
                mensaje.color = ft.Colors.GREEN

        except Exception as error:
            mensaje.value = (
                f"Error al consultar categorías: {error}"
            )
            mensaje.color = ft.Colors.RED

    def guardar_categoria(e):

        nombre = nombre_input.value
        descripcion = descripcion_input.value

        if nombre == "" or descripcion == "":
            mensaje.value = (
                "Nombre y descripción son obligatorios"
            )
            mensaje.color = ft.Colors.RED

            e.control.page.update()
            return

        categoria = Categoria(
            id_categoria=categoria_seleccionada["id"],
            nombre=nombre,
            descripcion=descripcion
        )

        categoria_dao = CategoriaDAO()

        if categoria_seleccionada["id"] == 0:

            resultado = categoria_dao.insertar(
                categoria
            )

            texto_exito = (
                "Categoría registrada correctamente"
            )

        else:

            resultado = categoria_dao.actualizar(
                categoria
            )

            texto_exito = (
                "Categoría actualizada correctamente"
            )

        if resultado:

            mensaje.value = texto_exito
            mensaje.color = ft.Colors.GREEN

            limpiar_formulario()
            cargar_categorias()

        else:
            mensaje.value = (
                "No fue posible guardar la categoría"
            )
            mensaje.color = ft.Colors.RED

        e.control.page.update()

    cargar_categorias()

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
                                    "Categorías",
                                    size=27,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Organiza los productos "
                                    "del inventario",
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
                                    descripcion_input,

                                    ft.ElevatedButton(
                                        content=texto_boton,
                                        icon=ft.Icons.SAVE,
                                        bgcolor="#D4A017",
                                        color=ft.Colors.BLACK,
                                        on_click=guardar_categoria
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