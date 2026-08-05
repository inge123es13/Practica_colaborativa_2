from database.conexion import Conexion


class FacturaDAO:

    # ---------- GENERAR FACTURAS FALTANTES ----------

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

    # ---------- CONSULTAR FACTURAS ----------

    def obtener_facturas(self):

        conexion = None
        cursor = None

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

                    COALESCE(
                        SUM(dv.subtotal),
                        v.total - v.iva,
                        0
                    ) AS subtotal,

                    v.iva,
                    v.total,
                    v.metodo_pago,
                    f.estado,

                    COALESCE(
                        STRING_AGG(
                            p.nombre || ' x' ||
                            dv.cantidad::TEXT,
                            ', '
                            ORDER BY dv.id_detalle
                        ),
                        'Sin detalle migrado'
                    ) AS productos

                FROM facturas f

                INNER JOIN ventas v
                    ON v.id_venta = f.id_venta

                INNER JOIN clientes c
                    ON c.id_cliente = f.id_cliente

                LEFT JOIN detalle_venta dv
                    ON dv.id_venta = v.id_venta

                LEFT JOIN productos p
                    ON p.id_producto = dv.id_producto

                GROUP BY
                    f.id_factura,
                    f.folio,
                    f.fecha_factura,
                    f.id_venta,
                    c.nombre,
                    v.iva,
                    v.total,
                    v.metodo_pago,
                    f.estado

                ORDER BY f.id_factura DESC
            """)

            return cursor.fetchall()

        except Exception as error:

            print("Error al consultar facturas:")
            print(error)

            return []

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    # ---------- OBTENER FACTURA COMPLETA ----------

    def obtener_factura_completa(
        self,
        id_factura
    ):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return None, []

            cursor = conexion.cursor()

            # Encabezado, venta y cliente
            cursor.execute(
                """
                SELECT
                    f.id_factura,
                    f.folio,
                    f.fecha_factura,
                    f.estado,

                    v.id_venta,
                    v.fecha_venta,
                    v.metodo_pago,
                    v.iva,
                    v.total,
                    v.estado,

                    c.id_cliente,
                    c.nombre,
                    c.telefono,
                    c.direccion,
                    c.correo,

                    COALESCE(
                        (
                            SELECT SUM(
                                dv2.subtotal
                            )
                            FROM detalle_venta dv2
                            WHERE
                                dv2.id_venta =
                                v.id_venta
                        ),
                        v.total - v.iva,
                        0
                    ) AS subtotal

                FROM facturas f

                INNER JOIN ventas v
                    ON v.id_venta = f.id_venta

                INNER JOIN clientes c
                    ON c.id_cliente = f.id_cliente

                WHERE f.id_factura = %s
                """,
                (id_factura,)
            )

            registro = cursor.fetchone()

            if registro is None:
                return None, []

            factura = {
                "id_factura": registro[0],
                "folio": registro[1],
                "fecha_factura": registro[2],
                "estado_factura": registro[3],

                "id_venta": registro[4],
                "fecha_venta": registro[5],
                "metodo_pago": registro[6],
                "iva": registro[7],
                "total": registro[8],
                "estado_venta": registro[9],

                "id_cliente": registro[10],
                "cliente_nombre": registro[11],
                "cliente_telefono": registro[12],
                "cliente_direccion": registro[13],
                "cliente_correo": registro[14],

                "subtotal": registro[15]
            }

            # Productos de la factura
            cursor.execute(
                """
                SELECT
                    dv.id_detalle,
                    p.id_producto,
                    p.nombre,
                    p.marca,
                    p.talla,
                    dv.cantidad,

                    CASE
                        WHEN dv.cantidad > 0
                        THEN
                            dv.subtotal /
                            dv.cantidad
                        ELSE 0
                    END AS precio_unitario,

                    dv.subtotal

                FROM detalle_venta dv

                INNER JOIN productos p
                    ON p.id_producto =
                       dv.id_producto

                WHERE dv.id_venta = %s

                ORDER BY dv.id_detalle
                """,
                (factura["id_venta"],)
            )

            registros_detalles = cursor.fetchall()

            detalles = []

            for detalle in registros_detalles:

                detalles.append(
                    {
                        "id_detalle": detalle[0],
                        "id_producto": detalle[1],
                        "producto": detalle[2],
                        "marca": detalle[3],
                        "talla": detalle[4],
                        "cantidad": detalle[5],
                        "precio_unitario": detalle[6],
                        "subtotal": detalle[7]
                    }
                )

            return factura, detalles

        except Exception as error:

            print("Error al obtener factura completa:")
            print(error)

            return None, []

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()