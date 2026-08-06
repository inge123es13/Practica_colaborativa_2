def generar_pdf_factura(filename="factura.pdf"):
    """Genera un archivo PDF físico con la estructura de la factura."""
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()

    # Encabezado
    elements.append(Paragraph("<b>TIENDA SHECSPER</b>", styles['Title']))
    elements.append(Paragraph("RFC: SHEC800101XXX | Tel: 246-123-4567", styles['Normal']))
    elements.append(Paragraph("Fecha: 05/08/2026", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Datos de la Factura
    data = [
        ["Cant.", "Descripción", "P. Unitario", "Importe"],
        ["1", "Playera Deportiva Premium", "$ 350.00", "$ 350.00"],
        ["2", "Calzado Urbano Casual", "$ 850.00", "$ 1,700.00"],
        ["", "", "Subtotal:", "$ 2,050.00"],
        ["", "", "IVA (16%):", "$ 328.00"],
        ["", "", "TOTAL:", "$ 2,378.00"],
    ]

    t = Table(data, colWidths=[50, 260, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, 2), 0.5, colors.lightgrey),
        ('FONTNAME', (2, 3), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (2, 3), (-1, -1), 'RIGHT'),
    ]))
    
    elements.append(t)
    doc.build(elements)

def main(page: ft.Page):
    page.title = "Sistema de Facturación - Shecsper"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    def exportar_pdf(e):
        generar_pdf_factura("factura_shecsper.pdf")
        page.open(
            ft.SnackBar(
                content=ft.Text("¡Factura generada exitosamente como PDF!"),
                bgcolor=ft.Colors.GREEN_700,
            )
        )

    # Vista previa de la factura en pantalla
    factura_card = ft.Card(
        content=ft.Container(
            padding=25,
            content=ft.Column(
                controls=[
                    # Cabecera de la factura
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([
                                ft.Text("TIENDA SHECSPER", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text("Ropa y Calzado Urbano / Deportivo", size=12, color=ft.Colors.GREY_700),
                            ]),
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Text("FACTURA: #F-2026-001", weight=ft.FontWeight.BOLD),
                                    ft.Text("Fecha: 05/08/2026", size=12, color=ft.Colors.GREY_700),
                                ]
                            )
                        ]
                    ),
                    ft.Divider(height=20),
                    
                    # Tabla de productos
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Cant.")),
                            ft.DataColumn(ft.Text("Descripción")),
                            ft.DataColumn(ft.Text("P. Unitario"), numeric=True),
                            ft.DataColumn(ft.Text("Importe"), numeric=True),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("1")),
                                ft.DataCell(ft.Text("Playera Deportiva Premium")),
                                ft.DataCell(ft.Text("$350.00")),
                                ft.DataCell(ft.Text("$350.00")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("2")),
                                ft.DataCell(ft.Text("Calzado Urbano Casual")),
                                ft.DataCell(ft.Text("$850.00")),
                                ft.DataCell(ft.Text("$1,700.00")),
                            ]),
                        ],
                    ),
                    ft.Divider(height=20),

                    # Totales
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Container(
                                width=220,
                                content=ft.Column([
                                    ft.Row([ft.Text("Subtotal:"), ft.Text("$2,050.00")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Row([ft.Text("IVA (16%):"), ft.Text("$328.00")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Divider(height=10),
                                    ft.Row([
                                        ft.Text("Total:", weight=ft.FontWeight.BOLD, size=16),
                                        ft.Text("$2,378.00", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.GREEN_700)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ])
                            )
                        ]
                    ),
                    
                    # Acciones
                    ft.Container(height=15),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                "Descargar PDF",
                                icon=ft.Icons.PICTURE_IN_PICTURE_ROUNDED,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800, color=ft.Colors.WHITE),
                                on_click=exportar_pdf
                            )
                        ]
                    )
                ]
            )
        )
    )

    page.add(
        ft.Text("Vista Previa de la Factura", size=24, weight=ft.FontWeight.BOLD),
        factura_card
    )

ft.app(target=main)