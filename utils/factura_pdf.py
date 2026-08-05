import os
import webbrowser

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from xml.sax.saxutils import escape

from num2words import num2words

from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT
)
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


# ==================================================
# CONFIGURACIÓN DE LA TIENDA
# Cambia estos datos por los datos reales
# ==================================================

EMISOR_NOMBRE = "SHECSPER"
EMISOR_RFC = "RFC NO REGISTRADO"
EMISOR_DIRECCION = (
    "Terrenate, Tlaxcala, México"
)
EMISOR_TELEFONO = "Teléfono no registrado"
EMISOR_CORREO = "Correo no registrado"
EMISOR_REGIMEN = "Comprobante interno"

MONEDA = "MXN"
IVA_PORCENTAJE = Decimal("16.00")


# ==================================================
# RUTAS DEL PROYECTO
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_LOGO = (
    BASE_DIR
    / "assets"
    / "icons"
    / "logo_shecsper.jpeg"
)

CARPETA_FACTURAS = (
    BASE_DIR
    / "facturas_generadas"
)


# ==================================================
# COLORES
# ==================================================

COLOR_NEGRO = colors.HexColor("#111111")
COLOR_DORADO = colors.HexColor("#D4A017")
COLOR_ROJO = colors.HexColor("#E74C3C")
COLOR_GRIS = colors.HexColor("#F3F4F6")
COLOR_GRIS_OSCURO = colors.HexColor("#666666")
COLOR_BORDE = colors.HexColor("#D1D5DB")
COLOR_VERDE = colors.HexColor("#166534")
COLOR_BLANCO = colors.white


# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def texto_seguro(valor):

    if valor is None:
        return ""

    return escape(str(valor))


def formato_moneda(valor):

    if valor is None:
        valor = Decimal("0.00")

    numero = Decimal(str(valor))

    return f"${numero:,.2f}"


def convertir_total_a_letra(valor):

    total = Decimal(str(valor)).quantize(
        Decimal("0.01")
    )

    parte_entera = int(total)

    centavos = int(
        (
            total - Decimal(parte_entera)
        ) * 100
    )

    cantidad_letra = num2words(
        parte_entera,
        lang="es"
    ).upper()

    return (
        f"{cantidad_letra} PESOS "
        f"{centavos:02d}/100 M.N."
    )


def abrir_archivo(ruta):

    ruta = Path(ruta).resolve()

    try:

        if os.name == "nt":
            os.startfile(str(ruta))

        else:
            webbrowser.open(
                ruta.as_uri()
            )

    except Exception as error:

        print(
            "No fue posible abrir el PDF:"
        )

        print(error)


def agregar_pie_pagina(
    canvas,
    documento
):

    canvas.saveState()

    ancho_pagina = LETTER[0]

    canvas.setStrokeColor(
        COLOR_BORDE
    )

    canvas.line(
        2 * cm,
        1.6 * cm,
        ancho_pagina - 2 * cm,
        1.6 * cm
    )

    canvas.setFont(
        "Helvetica",
        7.5
    )

    canvas.setFillColor(
        COLOR_GRIS_OSCURO
    )

    canvas.drawString(
        2 * cm,
        1.15 * cm,
        (
            "Shecsper - Sistema local "
            "de inventario"
        )
    )

    canvas.drawRightString(
        ancho_pagina - 2 * cm,
        1.15 * cm,
        f"Página {documento.page}"
    )

    canvas.restoreState()


# ==================================================
# GENERAR PDF
# ==================================================

def generar_factura_pdf(
    factura,
    detalles
):

    CARPETA_FACTURAS.mkdir(
        parents=True,
        exist_ok=True
    )

    folio_seguro = (
        str(factura["folio"])
        .replace("/", "-")
        .replace("\\", "-")
        .replace(" ", "_")
    )

    ruta_pdf = (
        CARPETA_FACTURAS
        / f"Factura_{folio_seguro}.pdf"
    )

    documento = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=LETTER,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2.2 * cm,
        title=(
            f"Factura "
            f"{factura['folio']}"
        ),
        author=(
            "Sistema de Inventario "
            "Shecsper"
        )
    )

    estilos_base = getSampleStyleSheet()

    estilo_normal = ParagraphStyle(
        name="NormalFactura",
        parent=estilos_base["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=COLOR_NEGRO,
        alignment=TA_LEFT
    )

    estilo_pequeno = ParagraphStyle(
        name="PequenoFactura",
        parent=estilo_normal,
        fontSize=7.5,
        leading=10,
        textColor=COLOR_GRIS_OSCURO
    )

    estilo_titulo = ParagraphStyle(
        name="TituloFactura",
        parent=estilo_normal,
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=26,
        textColor=COLOR_NEGRO
    )

    estilo_subtitulo = ParagraphStyle(
        name="SubtituloFactura",
        parent=estilo_normal,
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=COLOR_DORADO
    )

    estilo_seccion = ParagraphStyle(
        name="SeccionFactura",
        parent=estilo_normal,
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=COLOR_NEGRO,
        spaceBefore=4,
        spaceAfter=5
    )

    estilo_derecha = ParagraphStyle(
        name="DerechaFactura",
        parent=estilo_normal,
        alignment=TA_RIGHT
    )

    estilo_centrado = ParagraphStyle(
        name="CentradoFactura",
        parent=estilo_normal,
        alignment=TA_CENTER
    )

    estilo_total = ParagraphStyle(
        name="TotalFactura",
        parent=estilo_normal,
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_RIGHT,
        textColor=COLOR_NEGRO
    )

    elementos = []

    # ==================================================
    # ENCABEZADO CON LOGOTIPO
    # ==================================================

    if RUTA_LOGO.exists():

        logo = Image(
            str(RUTA_LOGO),
            width=3.4 * cm,
            height=3.4 * cm
        )

    else:

        logo = Paragraph(
            "<b>LOGOTIPO</b>",
            estilo_centrado
        )

    datos_emisor = Paragraph(
        (
            f"<font size='17'>"
            f"<b>{texto_seguro(EMISOR_NOMBRE)}</b>"
            f"</font><br/>"
            f"<font color='#D4A017'>"
            f"<b>SISTEMA DE INVENTARIO</b>"
            f"</font><br/><br/>"
            f"<b>RFC:</b> "
            f"{texto_seguro(EMISOR_RFC)}<br/>"
            f"<b>Régimen:</b> "
            f"{texto_seguro(EMISOR_REGIMEN)}<br/>"
            f"<b>Dirección:</b> "
            f"{texto_seguro(EMISOR_DIRECCION)}<br/>"
            f"<b>Teléfono:</b> "
            f"{texto_seguro(EMISOR_TELEFONO)}<br/>"
            f"<b>Correo:</b> "
            f"{texto_seguro(EMISOR_CORREO)}"
        ),
        estilo_normal
    )

    datos_factura = Paragraph(
        (
            "<font size='17'>"
            "<b>FACTURA</b>"
            "</font><br/><br/>"
            f"<b>Folio:</b> "
            f"{texto_seguro(factura['folio'])}"
            f"<br/>"
            f"<b>Número:</b> "
            f"{factura['id_factura']}"
            f"<br/>"
            f"<b>Fecha de emisión:</b><br/>"
            f"{texto_seguro(factura['fecha_factura'])}"
            f"<br/>"
            f"<b>Venta relacionada:</b> "
            f"#{factura['id_venta']}"
            f"<br/>"
            f"<b>Moneda:</b> {MONEDA}"
        ),
        estilo_derecha
    )

    tabla_encabezado = Table(
        [
            [
                logo,
                datos_emisor,
                datos_factura
            ]
        ],
        colWidths=[
            3.8 * cm,
            8.7 * cm,
            5.5 * cm
        ]
    )

    tabla_encabezado.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    COLOR_NEGRO
                ),
                (
                    "LINEAFTER",
                    (1, 0),
                    (1, 0),
                    0.8,
                    COLOR_NEGRO
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, 0),
                    COLOR_GRIS
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(
        tabla_encabezado
    )

    elementos.append(
        Spacer(1, 12)
    )

    # ==================================================
    # DATOS DEL CLIENTE
    # ==================================================

    encabezado_cliente = Table(
        [
            [
                Paragraph(
                    "DATOS DEL CLIENTE",
                    estilo_seccion
                )
            ]
        ],
        colWidths=[18 * cm]
    )

    encabezado_cliente.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    COLOR_NEGRO
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    COLOR_BLANCO
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

    elementos.append(
        encabezado_cliente
    )

    cliente_nombre = texto_seguro(
        factura["cliente_nombre"]
    )

    cliente_telefono = texto_seguro(
        factura["cliente_telefono"]
        or "No registrado"
    )

    cliente_correo = texto_seguro(
        factura["cliente_correo"]
        or "No registrado"
    )

    cliente_direccion = texto_seguro(
        factura["cliente_direccion"]
        or "No registrada"
    )

    tabla_cliente = Table(
        [
            [
                Paragraph(
                    (
                        "<b>Nombre o razón social:</b><br/>"
                        f"{cliente_nombre}"
                    ),
                    estilo_normal
                ),
                Paragraph(
                    (
                        "<b>ID del cliente:</b><br/>"
                        f"{factura['id_cliente']}"
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        "<b>Dirección:</b><br/>"
                        f"{cliente_direccion}"
                    ),
                    estilo_normal
                ),
                Paragraph(
                    (
                        "<b>Teléfono:</b><br/>"
                        f"{cliente_telefono}"
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        "<b>Correo electrónico:</b><br/>"
                        f"{cliente_correo}"
                    ),
                    estilo_normal
                ),
                Paragraph(
                    (
                        "<b>Fecha de venta:</b><br/>"
                        f"{texto_seguro(factura['fecha_venta'])}"
                    ),
                    estilo_normal
                )
            ]
        ],
        colWidths=[
            12 * cm,
            6 * cm
        ]
    )

    tabla_cliente.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    elementos.append(
        tabla_cliente
    )

    elementos.append(
        Spacer(1, 12)
    )

    # ==================================================
    # PRODUCTOS
    # ==================================================

    encabezados_productos = [
        Paragraph(
            "<b>Cantidad</b>",
            estilo_centrado
        ),
        Paragraph(
            "<b>Descripción</b>",
            estilo_centrado
        ),
        Paragraph(
            "<b>Marca</b>",
            estilo_centrado
        ),
        Paragraph(
            "<b>Talla</b>",
            estilo_centrado
        ),
        Paragraph(
            "<b>Precio unitario</b>",
            estilo_centrado
        ),
        Paragraph(
            "<b>Importe</b>",
            estilo_centrado
        )
    ]

    datos_productos = [
        encabezados_productos
    ]

    for detalle in detalles:

        datos_productos.append(
            [
                Paragraph(
                    str(detalle["cantidad"]),
                    estilo_centrado
                ),
                Paragraph(
                    texto_seguro(
                        detalle["producto"]
                    ),
                    estilo_normal
                ),
                Paragraph(
                    texto_seguro(
                        detalle["marca"]
                        or "-"
                    ),
                    estilo_centrado
                ),
                Paragraph(
                    texto_seguro(
                        detalle["talla"]
                        or "-"
                    ),
                    estilo_centrado
                ),
                Paragraph(
                    formato_moneda(
                        detalle["precio_unitario"]
                    ),
                    estilo_derecha
                ),
                Paragraph(
                    formato_moneda(
                        detalle["subtotal"]
                    ),
                    estilo_derecha
                )
            ]
        )

    if len(detalles) == 0:

        datos_productos.append(
            [
                Paragraph(
                    "-",
                    estilo_centrado
                ),
                Paragraph(
                    (
                        "Venta antigua sin "
                        "detalle de productos migrado"
                    ),
                    estilo_normal
                ),
                Paragraph("-", estilo_centrado),
                Paragraph("-", estilo_centrado),
                Paragraph("-", estilo_derecha),
                Paragraph(
                    formato_moneda(
                        factura["subtotal"]
                    ),
                    estilo_derecha
                )
            ]
        )

    tabla_productos = Table(
        datos_productos,
        colWidths=[
            1.7 * cm,
            5.5 * cm,
            2.6 * cm,
            1.8 * cm,
            3.1 * cm,
            3.3 * cm
        ],
        repeatRows=1
    )

    tabla_productos.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    COLOR_NEGRO
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    COLOR_BLANCO
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        COLOR_BLANCO,
                        COLOR_GRIS
                    ]
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(
        tabla_productos
    )

    elementos.append(
        Spacer(1, 12)
    )

    # ==================================================
    # INFORMACIÓN DE PAGO Y TOTALES
    # ==================================================

    metodo_pago = texto_seguro(
        factura["metodo_pago"]
    )

    estado_venta = texto_seguro(
        factura["estado_venta"]
    )

    estado_factura = texto_seguro(
        factura["estado_factura"]
    )

    total_letra = convertir_total_a_letra(
        factura["total"]
    )

    datos_pago = Table(
        [
            [
                Paragraph(
                    "<b>INFORMACIÓN DE PAGO</b>",
                    estilo_seccion
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Método de pago:</b> "
                        f"{metodo_pago}"
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Moneda:</b> "
                        f"{MONEDA}"
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Estado de venta:</b> "
                        f"{estado_venta}"
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Estado de factura:</b> "
                        f"{estado_factura}"
                    ),
                    estilo_normal
                )
            ]
        ],
        colWidths=[10.5 * cm]
    )

    datos_pago.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    COLOR_NEGRO
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    COLOR_BLANCO
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    tabla_totales = Table(
        [
            [
                Paragraph(
                    "<b>Subtotal:</b>",
                    estilo_derecha
                ),
                Paragraph(
                    formato_moneda(
                        factura["subtotal"]
                    ),
                    estilo_derecha
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>IVA "
                        f"{IVA_PORCENTAJE}%:</b>"
                    ),
                    estilo_derecha
                ),
                Paragraph(
                    formato_moneda(
                        factura["iva"]
                    ),
                    estilo_derecha
                )
            ],
            [
                Paragraph(
                    "<b>TOTAL:</b>",
                    estilo_total
                ),
                Paragraph(
                    (
                        f"<b>"
                        f"{formato_moneda(factura['total'])}"
                        f"</b>"
                    ),
                    estilo_total
                )
            ]
        ],
        colWidths=[
            3.5 * cm,
            4 * cm
        ]
    )

    tabla_totales.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "BACKGROUND",
                    (0, 2),
                    (-1, 2),
                    COLOR_DORADO
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    contenedor_pago_totales = Table(
        [
            [
                datos_pago,
                tabla_totales
            ]
        ],
        colWidths=[
            10.5 * cm,
            7.5 * cm
        ]
    )

    contenedor_pago_totales.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                )
            ]
        )
    )

    elementos.append(
        contenedor_pago_totales
    )

    elementos.append(
        Spacer(1, 12)
    )

    # ==================================================
    # IMPORTE CON LETRA
    # ==================================================

    tabla_letra = Table(
        [
            [
                Paragraph(
                    "<b>Importe con letra:</b>",
                    estilo_normal
                ),
                Paragraph(
                    texto_seguro(total_letra),
                    estilo_normal
                )
            ]
        ],
        colWidths=[
            3.4 * cm,
            14.6 * cm
        ]
    )

    tabla_letra.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    COLOR_NEGRO
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, 0),
                    COLOR_BLANCO
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(
        tabla_letra
    )

    elementos.append(
        Spacer(1, 14)
    )

    # ==================================================
    # OBSERVACIONES
    # ==================================================

    observaciones = Table(
        [
            [
                Paragraph(
                    "<b>OBSERVACIONES</b>",
                    estilo_seccion
                )
            ],
            [
                Paragraph(
                    (
                        "Gracias por su compra. "
                        "Conserve este comprobante "
                        "para cualquier aclaración."
                    ),
                    estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        "Este documento fue generado "
                        "automáticamente por el sistema "
                        "local de inventario Shecsper."
                    ),
                    estilo_pequeno
                )
            ],
            [
                Paragraph(
                    (
                        "<b>Documento interno sin "
                        "validez fiscal ante el SAT.</b>"
                    ),
                    ParagraphStyle(
                        name="AvisoFiscal",
                        parent=estilo_normal,
                        fontName="Helvetica-Bold",
                        fontSize=8,
                        textColor=COLOR_ROJO,
                        alignment=TA_CENTER
                    )
                )
            ]
        ],
        colWidths=[18 * cm]
    )

    observaciones.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    COLOR_NEGRO
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    COLOR_BLANCO
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDE
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    elementos.append(
        observaciones
    )

    # ==================================================
    # CREAR ARCHIVO
    # ==================================================

    documento.build(
        elementos,
        onFirstPage=agregar_pie_pagina,
        onLaterPages=agregar_pie_pagina
    )

    abrir_archivo(
        ruta_pdf
    )

    return str(
        ruta_pdf.resolve()
    )