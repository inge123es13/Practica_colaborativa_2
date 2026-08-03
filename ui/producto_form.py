import flet as ft

from dao.categoria_dao import CategoriaDAO
from dao.producto_dao import ProductoDAO
from models.producto import Producto


def producto_form(regresar, producto=None):

    editando = producto is not None

    nombre_input = ft.TextField(
        label="Nombre del producto",
        width=350,
        value=producto.nombre if editando else ""
    )

    descripcion_input = ft.TextField(
        label="Descripción",
        width=350,
        multiline=True,
        value=producto.descripcion if editando else ""
    )

    precio_input = ft.TextField(
        label="Precio",
        width=200,
        value=str(producto.precio) if editando else ""
    )

    stock_input = ft.TextField(
        label="Stock disponible",
        width=200,
        value=str(producto.stock_actual) if editando else ""
    )

    marca_input = ft.TextField(
        label="Marca",
        width=250,
        value=producto.marca if editando else ""
    )

    talla_input = ft.TextField(
        label="Talla",
        width=150,
        value=producto.talla if editando else ""
    )

    mensaje = ft.Text("")

    # Obtener las categorías desde PostgreSQL
    categoria_dao = CategoriaDAO()
    categorias = categoria_dao.obtener_categorias()

    opciones_categorias = []

    for categoria in categorias:
        opciones_categorias.append(
            ft.DropdownOption(
                key=str(categoria.id_categoria),
                text=categoria.nombre
            )
        )

    categoria_input = ft.Dropdown(
        label="Categoría",
        width=220,
        options=opciones_categorias,
        value=(
            str(producto.id_categoria)
            if editando
            else None
        )
    )

    def guardar_producto(e):

        nombre = nombre_input.value
        descripcion = descripcion_input.value
        precio = precio_input.value
        stock = stock_input.value
        marca = marca_input.value
        talla = talla_input.value
        categoria = categoria_input.value

        if (
            nombre == ""
            or descripcion == ""
            or precio == ""
            or stock == ""
            or marca == ""
            or talla == ""
            or categoria is None
            or categoria == ""
        ):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            e.control.page.update()
            return

        try:
            id_producto = (
                producto.id_producto
                if editando
                else 0
            )

            producto_guardar = Producto(
                id_producto=id_producto,
                nombre=nombre,
                descripcion=descripcion,
                precio=float(precio),
                stock_actual=int(stock),
                marca=marca,
                talla=talla,
                id_categoria=int(categoria)
            )

            producto_dao = ProductoDAO()

            if editando:

                producto_dao.actualizar(
                    producto_guardar
                )

                mensaje.value = (
                    f"Producto '{nombre}' "
                    "actualizado correctamente"
                )

            else:

                producto_dao.insertar(
                    producto_guardar
                )

                mensaje.value = (
                    f"Producto '{nombre}' "
                    "registrado correctamente"
                )

                nombre_input.value = ""
                descripcion_input.value = ""
                precio_input.value = ""
                stock_input.value = ""
                marca_input.value = ""
                talla_input.value = ""
                categoria_input.value = None

            mensaje.color = ft.Colors.GREEN

        except ValueError:

            mensaje.value = (
                "Precio y stock deben ser números válidos"
            )
            mensaje.color = ft.Colors.RED

        except Exception as error:

            mensaje.value = (
                f"Error al guardar el producto: {error}"
            )
            mensaje.color = ft.Colors.RED

        e.control.page.update()

    titulo = (
        "Editar producto"
        if editando
        else "Registrar nuevo producto"
    )

    texto_boton = (
        "Actualizar producto"
        if editando
        else "Guardar producto"
    )

    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    titulo,
                    size=27,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Captura la información de la mercancía",
                    color=ft.Colors.GREY_700
                ),

                ft.Container(
                    width=70,
                    height=4,
                    bgcolor="#E74C3C"
                ),

                ft.Row(
                    controls=[
                        nombre_input,
                        marca_input,
                        talla_input
                    ],
                    wrap=True
                ),

                ft.Row(
                    controls=[
                        descripcion_input,
                        precio_input,
                        stock_input,
                        categoria_input
                    ],
                    wrap=True
                ),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content=ft.Text(texto_boton),
                            icon=ft.Icons.SAVE,
                            bgcolor="#D4A017",
                            color=ft.Colors.BLACK,
                            on_click=guardar_producto
                        ),

                        ft.OutlinedButton(
                            content=ft.Text("Regresar"),
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: regresar()
                        )
                    ]
                ),

                mensaje
            ],
            spacing=18,
            scroll=ft.ScrollMode.AUTO
        )
    )