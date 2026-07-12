from database.conexion import obtener_conexion
from models.producto import Producto

class ProductoDAO:
    @staticmethod
    def listar_todos():
        conexion = obtener_conexion()
        if not conexion: return []
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_producto, nombre, descripcion, precio, stock_actual, marca, talla, id_categoria FROM productos ORDER BY id_producto;")
            return [Producto(f[0], f[1], f[2], float(f[3]), f[4], f[5], f[6], f[7]) for f in cursor.fetchall()]
        except Exception as e:
            print(f"Error al listar productos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def insertar(producto):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """INSERT INTO productos (nombre, descripcion, precio, stock_actual, marca, talla, id_categoria) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                (producto.nombre, producto.descripcion, producto.precio, producto.stock_actual, producto.marca, producto.talla, producto.id_categoria)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar producto: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(producto):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock_actual=%s, marca=%s, talla=%s, id_categoria=%s 
                   WHERE id_producto=%s;""",
                (producto.nombre, producto.descripcion, producto.precio, producto.stock_actual, producto.marca, producto.talla, producto.id_categoria, producto.id_producto)
            )
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_producto):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE id_producto=%s;", (id_producto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()