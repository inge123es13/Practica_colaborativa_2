from decimal import Decimal, ROUND_HALF_UP

from database.conexion import Conexion
from models.venta import Venta


class VentaDAO:

    def obtener_ventas(self):
        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_venta,
                    id_usuario,
                    id_cliente,
                    fecha_venta,
                    metodo_pago,
                    iva,
                    total,
                    estado
                FROM ventas
                ORDER BY id_venta DESC
            """)

            registros = cursor.fetchall()
            ventas = []

            for registro in registros:
                venta = Venta(
                    id_venta=registro[0],
                    id_usuario=registro[1],
                    id_cliente=registro[2],
                    fecha_venta=registro[3],
                    metodo_pago=registro[4],
                    iva=registro[5],
                    total=registro[6],
                    estado=registro[7]
                )

                ventas.append(venta)

            return ventas

        except Exception as error:
            print(f"Error al obtener las ventas: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def registrar_venta(self, venta, detalles):
        conexion = None
        cursor = None

        try:
            if not detalles:
                raise ValueError(
                    "La venta debe contener por lo menos un producto."
                )

            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            detalles_calculados = []
            subtotal_general = Decimal("0.00")

            # Validar productos, obtener precios y bloquear el stock
            for detalle in detalles:

                if detalle.cantidad <= 0:
                    raise ValueError(
                        "La cantidad debe ser mayor que cero."
                    )

                cursor.execute("""
                    SELECT precio, stock_actual
                    FROM productos
                    WHERE id_producto = %s
                    FOR UPDATE
                """, (detalle.id_producto,))

                producto = cursor.fetchone()

                if producto is None:
                    raise ValueError(
                        f"No existe el producto {detalle.id_producto}."
                    )

                precio = Decimal(str(producto[0]))
                stock_actual = producto[1]

                if stock_actual < detalle.cantidad:
                    raise ValueError(
                        f"Stock insuficiente para el producto "
                        f"{detalle.id_producto}. "
                        f"Disponible: {stock_actual}."
                    )

                subtotal = (
                    precio * Decimal(detalle.cantidad)
                ).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )

                detalle.subtotal = subtotal
                subtotal_general += subtotal

                detalles_calculados.append(detalle)

            # Calcular IVA y total general
            iva = (
                subtotal_general * Decimal("0.16")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            total = subtotal_general + iva

            venta.iva = iva
            venta.total = total

            # Registrar encabezado de la venta
            cursor.execute("""
                INSERT INTO ventas (
                    id_usuario,
                    id_cliente,
                    fecha_venta,
                    metodo_pago,
                    iva,
                    total,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_venta
            """, (
                venta.id_usuario,
                venta.id_cliente,
                venta.fecha_venta,
                venta.metodo_pago,
                venta.iva,
                venta.total,
                venta.estado
            ))

            id_venta = cursor.fetchone()[0]
            venta.id_venta = id_venta

            # Registrar productos y descontar existencias
            for detalle in detalles_calculados:
                detalle.id_venta = id_venta

                cursor.execute("""
                    INSERT INTO detalle_venta (
                        id_venta,
                        id_producto,
                        cantidad,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_detalle
                """, (
                    detalle.id_venta,
                    detalle.id_producto,
                    detalle.cantidad,
                    detalle.subtotal
                ))

                detalle.id_detalle = cursor.fetchone()[0]

                cursor.execute("""
                    UPDATE productos
                    SET stock_actual = stock_actual - %s
                    WHERE id_producto = %s
                """, (
                    detalle.cantidad,
                    detalle.id_producto
                ))

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

    # Permite seguir utilizando venta_dao.insertar(...)
    def insertar(self, venta, detalles):
        return self.registrar_venta(venta, detalles)