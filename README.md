# Sistema de Inventario Shecsper

Sistema de software local desarrollado para administrar la información interna de la tienda Shecsper.

## Integrantes

- Ingrid Estefany Gómez Pérez
- Jesús López de Fermín

## Objetivo

Administrar productos, categorías, clientes, usuarios, ventas y facturas mediante una aplicación gráfica conectada con PostgreSQL.

## Tecnologías utilizadas

- Python
- Flet
- PostgreSQL
- psycopg2
- python-dotenv
- Visual Studio Code
- pgAdmin 4

## Funciones principales

- Inicio y cierre de sesión.
- Acceso según el rol de administrador o empleado.
- Registro, consulta, modificación y eliminación de productos.
- Consulta de productos por nombre, categoría, marca y talla.
- Control de existencias y alertas de stock bajo.
- Registro y modificación de categorías.
- Administración de clientes.
- Administración de usuarios y roles.
- Registro de ventas.
- Descuento automático del stock.
- Cálculo de subtotal, IVA y total.
- Generación automática de facturas.
- Panel principal con resumen del inventario.

## Estructura del proyecto

```text
tienda_ropa/
├── assets/
│   └── icons/
├── dao/
├── database/
├── models/
├── ui/
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirements.txt