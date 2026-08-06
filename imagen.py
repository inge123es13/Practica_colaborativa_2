import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de Imagen en Flet"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. Cargar una imagen desde una URL
    imagen_url = ft.Image(
        src="https://picsum.photos/300/200",
        width=300,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(10),
    )

    # 2. Cargar una imagen desde una ruta local
    # (Asegúrate de cambiar "mi_imagen.png" por la ruta de tu imagen)
    imagen_local = ft.Image(
        src="assets/mi_imagen.png", # O usa la ruta relativa/absoluta ej: "imagen.jpg"
        width=300,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    page.add(
        ft.Text("Imagen desde URL:", weight=ft.FontWeight.BOLD),
        imagen_url,
        ft.Divider(),
        ft.Text("Imagen Local:", weight=ft.FontWeight.BOLD),
        imagen_local,
    )

ft.app(target=main)