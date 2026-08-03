from database.conexion import Conexion


class FacturaDAO:

    def generar_facturas_faltantes(self):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return 0

            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO facturas(
                    id_venta,
                    id_cliente,
                    fecha_factura,
                    folio,
                    estado
                )
                SELECT
                    v.id_venta,
                    v.id_cliente,
                    CURRENT_DATE,
                    'SH-' || LPAD(
                        v.id_venta::TEXT,
                        6,
                        '0'
                    ),
                    'Emitida'
                FROM ventas v
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM facturas f
                    WHERE f.id_venta = v.id_venta
                )
            """)

            cantidad = cursor.rowcount

            conexion.commit()

            return cantidad

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al generar facturas:")
            print(error)

            return 0

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def obtener_facturas(self):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    f.id_factura,
                    f.folio,
                    f.fecha_factura,
                    f.id_venta,
                    c.nombre,
                    v.subtotal,
                    v.iva,
                    v.total,
                    v.metodo_pago,
                    f.estado
                FROM facturas f
                INNER JOIN ventas v
                    ON v.id_venta = f.id_venta
                INNER JOIN clientes c
                    ON c.id_cliente = f.id_cliente
                ORDER BY f.id_factura DESC
            """)

            facturas = cursor.fetchall()

            cursor.close()
            conexion.close()

            return facturas

        except Exception as error:
            print("Error al consultar facturas:")
            print(error)

            return []