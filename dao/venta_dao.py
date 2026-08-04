from decimal import Decimal

from database.conexion import Conexion


class VentaDAO:

    def obtener_ventas(self):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    v.id_venta,
                    v.fecha_venta,
                    u.nombre,
                    c.nombre,
                    COALESCE(p.nombre, 'Sin producto'),
                    v.cantidad,
                    v.precio_unitario,
                    v.total,
                    v.metodo_pago,
                    v.estado
                FROM ventas v
                INNER JOIN usuarios u
                    ON u.id_usuario = v.id_usuario
                INNER JOIN clientes c
                    ON c.id_cliente = v.id_cliente
                LEFT JOIN productos p
                    ON p.id_producto = v.id_producto
                ORDER BY v.id_venta DESC
            """)

            ventas = cursor.fetchall()

            cursor.close()
            conexion.close()

            return ventas

        except Exception as error:
            print("Error al consultar ventas:")
            print(error)

            return []

    def registrar(self, venta):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                raise Exception(
                    "No fue posible conectar con PostgreSQL"
                )

            cursor = conexion.cursor()

            # Obtener y bloquear el producto
            cursor.execute(
                """
                SELECT
                    precio,
                    stock_actual
                FROM productos
                WHERE id_producto = %s
                FOR UPDATE
                """,
                (venta.id_producto,)
            )

            producto = cursor.fetchone()

            if producto is None:
                raise ValueError(
                    "El producto seleccionado no existe"
                )

            precio_unitario = producto[0]
            stock_actual = producto[1]

            if venta.cantidad <= 0:
                raise ValueError(
                    "La cantidad debe ser mayor que cero"
                )

            if venta.cantidad > stock_actual:
                raise ValueError(
                    f"Stock insuficiente. "
                    f"Existencias disponibles: {stock_actual}"
                )

            # Calcular los importes
            subtotal = (
                precio_unitario * venta.cantidad
            )

            iva = (
                subtotal * Decimal("0.16")
            )

            total = subtotal + iva

            # Registrar la venta
            cursor.execute(
                """
                INSERT INTO ventas(
                    id_usuario,
                    id_cliente,
                    fecha_venta,
                    metodo_pago,
                    subtotal,
                    iva,
                    total,
                    estado,
                    id_producto,
                    cantidad,
                    precio_unitario
                )
                VALUES (
                    %s,
                    %s,
                    CURRENT_DATE,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id_venta
                """,
                (
                    venta.id_usuario,
                    venta.id_cliente,
                    venta.metodo_pago,
                    subtotal,
                    iva,
                    total,
                    venta.estado,
                    venta.id_producto,
                    venta.cantidad,
                    precio_unitario
                )
            )

            id_venta = cursor.fetchone()[0]

            # Descontar las existencias
            cursor.execute(
                """
                UPDATE productos
                SET stock_actual = stock_actual - %s
                WHERE id_producto = %s
                """,
                (
                    venta.cantidad,
                    venta.id_producto
                )
            )

            # Crear el folio de la factura
            folio = f"SH-{id_venta:06d}"

            # Generar la factura
            cursor.execute(
                """
                INSERT INTO facturas(
                    id_venta,
                    id_cliente,
                    fecha_factura,
                    folio,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    CURRENT_DATE,
                    %s,
                    %s
                )
                """,
                (
                    id_venta,
                    venta.id_cliente,
                    folio,
                    "Emitida"
                )
            )

            # Guardar venta, stock y factura juntos
            conexion.commit()

            return id_venta

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            raise error

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()