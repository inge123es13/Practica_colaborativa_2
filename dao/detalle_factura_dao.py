from database.conexion import Conexion
from models.detalle_factura import DetalleFactura

class DetalleFacturaDAO:

    def obtener_detalles_por_factura(self, id_factura):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        sql = """
            SELECT id_detalle, cantidad, precio_unitario, subtotal, id_factura, id_producto 
            FROM detalle_factura 
            WHERE id_factura = %s 
            ORDER BY id_detalle
        """
        cursor.execute(sql, (id_factura,))
        registros = cursor.fetchall()

        detalles = []
        for reg in registros:
            det = DetalleFactura(
                id_detalle=reg[0],
                cantidad=reg[1],
                precio_unitario=reg[2],
                subtotal=reg[3],
                id_factura=reg[4],
                id_producto=reg[5]
            )
            detalles.append(det)
            
        cursor.close()
        conexion.close()
        return detalles
    
    def insertar(self, detalle):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO detalle_factura(cantidad, precio_unitario, subtotal, id_factura, id_producto)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            detalle.cantidad,
            detalle.precio_unitario,
            detalle.subtotal,
            detalle.id_factura,
            detalle.id_producto
        ))

        conexion.commit()
        cursor.close()
        conexion.close()