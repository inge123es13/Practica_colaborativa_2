import flet as ft

from dao.categoria_dao import CategoriaDAO
from dao.producto_dao import ProductoDAO


def productos_list(
    regresar,
    nuevo_producto,
    editar_producto
):

    busqueda_input = ft.TextField(
        label="Buscar por nombre",
        width=260,
        prefix_icon=ft.Icons.SEARCH
    )

    marca_input = ft.TextField(
        label="Marca",
        width=200
    )

    talla_input = ft.TextField(
        label="Talla",
        width=150
    )

    categorias = CategoriaDAO().obtener_categorias()

    nombres_categorias = {
        categoria.id_categoria: categoria.nombre
        for categoria in categorias
    }

    opciones_categorias = [
        ft.DropdownOption(
            key="0",
            text="Todas las categorías"
        )
    ]

    for categoria in categorias:

        opciones_categorias.append(
            ft.DropdownOption(
                key=str(categoria.id_categoria),
                text=categoria.nombre
            )
        )

    categoria_input = ft.Dropdown(
        label="Categoría",
        width=240,
        value="0",
        options=opciones_categorias
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Talla")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    mensaje = ft.Text("")

    def cargar_productos(e=None):

        try:
            id_categoria = None

            if (
                categoria_input.value is not None
                and categoria_input.value != "0"
            ):
                id_categoria = int(
                    categoria_input.value
                )

            producto_dao = ProductoDAO()

            productos = producto_dao.obtener_productos(
                busqueda=busqueda_input.value or "",
                id_categoria=id_categoria,
                marca=marca_input.value or "",
                talla=talla_input.value or ""
            )

            tabla.rows.clear()

            for producto in productos:

                if producto.stock_actual == 0:
                    color_stock = ft.Colors.RED

                elif producto.stock_actual <= 5:
                    color_stock = "#D4A017"

                else:
                    color_stock = ft.Colors.GREEN

                nombre_categoria = (
                    nombres_categorias.get(
                        producto.id_categoria,
                        str(producto.id_categoria)
                    )
                )

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(producto.id_producto)
                                )
                            ),

                            ft.DataCell(
                                ft.Text(producto.nombre)
                            ),

                            ft.DataCell(
                                ft.Text(producto.descripcion)
                            ),

                            ft.DataCell(
                                ft.Text(
                                    f"${producto.precio:.2f}"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(producto.stock_actual),
                                    color=color_stock,
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.DataCell(
                                ft.Text(producto.marca)
                            ),

                            ft.DataCell(
                                ft.Text(producto.talla)
                            ),

                            ft.DataCell(
                                ft.Text(nombre_categoria)
                            ),

                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="#D4A017",
                                            tooltip="Editar producto",
                                            on_click=lambda e, p=producto:
                                                editar_producto(p)
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            tooltip="Eliminar producto",
                                            on_click=lambda e, p=producto:
                                                confirmar_eliminacion(
                                                    e,
                                                    p
                                                )
                                        )
                                    ]
                                )
                            ),
                        ]
                    )
                )

            if len(productos) == 0:
                mensaje.value = (
                    "No se encontraron productos"
                )
                mensaje.color = ft.Colors.RED

            else:
                mensaje.value = (
                    f"Productos encontrados: "
                    f"{len(productos)}"
                )
                mensaje.color = ft.Colors.GREEN

            if e is not None:
                e.control.page.update()

        except Exception as error:
            mensaje.value = (
                f"Error al consultar productos: {error}"
            )
            mensaje.color = ft.Colors.RED

            if e is not None:
                e.control.page.update()

    def limpiar_filtros(e):

        busqueda_input.value = ""
        marca_input.value = ""
        talla_input.value = ""
        categoria_input.value = "0"

        cargar_productos()

        e.control.page.update()

    def confirmar_eliminacion(e, producto):

        page = e.control.page

        def cancelar(e):
            page.pop_dialog()

        def eliminar(e):

            page.pop_dialog()

            try:
                ProductoDAO().eliminar(
                    producto.id_producto
                )

                mensaje.value = (
                    f"Producto '{producto.nombre}' "
                    "eliminado correctamente"
                )
                mensaje.color = ft.Colors.GREEN

                cargar_productos()

            except Exception:
                mensaje.value = (
                    "No se pudo eliminar el producto. "
                    "Puede estar relacionado con una venta."
                )
                mensaje.color = ft.Colors.RED

            page.update()

        ventana = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar producto"),
            content=ft.Text(
                f"¿Realmente deseas eliminar "
                f"'{producto.nombre}'?"
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

    cargar_productos()

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
                                    "Inventario de productos",
                                    size=26,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "Consulta y filtra las "
                                    "existencias de Shecsper",
                                    color=ft.Colors.GREY_700
                                ),
                            ]
                        ),

                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "Nuevo producto"
                                    ),
                                    icon=ft.Icons.ADD,
                                    bgcolor="#D4A017",
                                    color=ft.Colors.BLACK,
                                    on_click=lambda e:
                                        nuevo_producto()
                                ),

                                ft.OutlinedButton(
                                    content=ft.Text("Regresar"),
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda e: regresar()
                                )
                            ]
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
                    padding=18,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    border=ft.Border.all(
                        1,
                        ft.Colors.GREY_300
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Filtros de búsqueda",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Row(
                                controls=[
                                    busqueda_input,
                                    categoria_input,
                                    marca_input,
                                    talla_input,

                                    ft.ElevatedButton(
                                        content=ft.Text("Buscar"),
                                        icon=ft.Icons.SEARCH,
                                        bgcolor="#D4A017",
                                        color=ft.Colors.BLACK,
                                        on_click=cargar_productos
                                    ),

                                    ft.OutlinedButton(
                                        content=ft.Text("Limpiar"),
                                        icon=ft.Icons.CLEAR,
                                        on_click=limpiar_filtros
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