from database.conexion import Conexion
from models.detalle_venta import DetalleVenta


class DetalleVentaDAO:

    def obtener_detalles(self):
        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_detalle,
                    id_venta,
                    id_producto,
                    cantidad,
                    subtotal
                FROM detalle_venta
                ORDER BY id_detalle
            """)

            registros = cursor.fetchall()
            detalles = []

            for registro in registros:
                detalle = DetalleVenta(
                    id_detalle=registro[0],
                    id_venta=registro[1],
                    id_producto=registro[2],
                    cantidad=registro[3],
                    subtotal=registro[4]
                )

                detalles.append(detalle)

            return detalles

        except Exception as error:
            print(f"Error al obtener los detalles: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def obtener_por_venta(self, id_venta):
        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_detalle,
                    id_venta,
                    id_producto,
                    cantidad,
                    subtotal
                FROM detalle_venta
                WHERE id_venta = %s
                ORDER BY id_detalle
            """, (id_venta,))

            registros = cursor.fetchall()
            detalles = []

            for registro in registros:
                detalle = DetalleVenta(
                    id_detalle=registro[0],
                    id_venta=registro[1],
                    id_producto=registro[2],
                    cantidad=registro[3],
                    subtotal=registro[4]
                )

                detalles.append(detalle)

            return detalles

        except Exception as error:
            print(f"Error al obtener el detalle de la venta: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()