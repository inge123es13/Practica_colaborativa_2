from database.conexion import Conexion
from models.factura import Factura

class FacturaDAO:

    def obtener_facturas(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_factura, fecha_factura, subtotal, iva, total, metodo_pago, estado, id_usuario 
            FROM facturas 
            ORDER BY id_factura
        """)
        registros = cursor.fetchall()

        facturas = []
        for reg in registros:
            fac = Factura(
                id_factura=reg[0],
                fecha_factura=reg[1],
                subtotal=reg[2],
                iva=reg[3],
                total=reg[4],
                metodo_pago=reg[5],
                estado=reg[6],
                id_usuario=reg[7]
            )
            facturas.append(fac)
            
        cursor.close()
        conexion.close()
        return facturas
    
    def insertar(self, factura):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        # Usamos RETURNING para capturar el ID generado automáticamente por la BD
        sql = """
        INSERT INTO facturas(fecha_factura, subtotal, iva, total, metodo_pago, estado, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_factura
        """
        cursor.execute(sql, (
            factura.fecha_factura,
            factura.subtotal,
            factura.iva,
            factura.total,
            factura.metodo_pago,
            factura.estado,
            factura.id_usuario
        ))
        
        id_generado = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
        conexion.close()
        return id_generado

    def cambiar_estado(self, id_factura, nuevo_estado):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE facturas SET estado = %s WHERE id_factura = %s"
        cursor.execute(sql, (nuevo_estado, id_factura))
        conexion.commit()
        cursor.close()
        conexion.close()