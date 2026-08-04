from database.conexion import Conexion
from models.producto import Producto


class ProductoDAO:

    def obtener_productos(
        self,
        busqueda="",
        id_categoria=None,
        marca="",
        talla=""
    ):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            patron_nombre = f"%{busqueda}%"
            patron_marca = f"%{marca}%"

            cursor.execute(
                """
                SELECT
                    id_producto,
                    nombre,
                    descripcion,
                    precio,
                    stock_actual,
                    marca,
                    talla,
                    id_categoria
                FROM productos
                WHERE (
                    %s = ''
                    OR nombre ILIKE %s
                )
                AND (
                    %s IS NULL
                    OR id_categoria = %s
                )
                AND (
                    %s = ''
                    OR marca ILIKE %s
                )
                AND (
                    %s = ''
                    OR talla ILIKE %s
                )
                ORDER BY id_producto
                """,
                (
                    busqueda,
                    patron_nombre,
                    id_categoria,
                    id_categoria,
                    marca,
                    patron_marca,
                    talla,
                    talla
                )
            )

            registros = cursor.fetchall()
            productos = []

            for registro in registros:

                producto = Producto(
                    id_producto=registro[0],
                    nombre=registro[1],
                    descripcion=registro[2],
                    precio=registro[3],
                    stock_actual=registro[4],
                    marca=registro[5],
                    talla=registro[6],
                    id_categoria=registro[7]
                )

                productos.append(producto)

            return productos

        except Exception as error:
            print("Error al obtener los productos:")
            print(error)

            return []

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def obtener_resumen(self):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return {
                    "productos": 0,
                    "existencias": 0,
                    "stock_bajo": 0,
                    "agotados": 0
                }

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*),

                    COALESCE(
                        SUM(stock_actual),
                        0
                    ),

                    COUNT(*) FILTER (
                        WHERE stock_actual BETWEEN 1 AND 5
                    ),

                    COUNT(*) FILTER (
                        WHERE stock_actual = 0
                    )
                FROM productos
            """)

            resultado = cursor.fetchone()

            return {
                "productos": resultado[0],
                "existencias": resultado[1],
                "stock_bajo": resultado[2],
                "agotados": resultado[3]
            }

        except Exception as error:
            print("Error al obtener el resumen:")
            print(error)

            return {
                "productos": 0,
                "existencias": 0,
                "stock_bajo": 0,
                "agotados": 0
            }

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def insertar(self, producto):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                raise Exception(
                    "No fue posible conectar con PostgreSQL"
                )

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO productos(
                    nombre,
                    descripcion,
                    precio,
                    stock_actual,
                    marca,
                    talla,
                    id_categoria
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    producto.nombre,
                    producto.descripcion,
                    producto.precio,
                    producto.stock_actual,
                    producto.marca,
                    producto.talla,
                    producto.id_categoria
                )
            )

            conexion.commit()

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            raise error

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def actualizar(self, producto):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                raise Exception(
                    "No fue posible conectar con PostgreSQL"
                )

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE productos
                SET nombre = %s,
                    descripcion = %s,
                    precio = %s,
                    stock_actual = %s,
                    marca = %s,
                    talla = %s,
                    id_categoria = %s
                WHERE id_producto = %s
                """,
                (
                    producto.nombre,
                    producto.descripcion,
                    producto.precio,
                    producto.stock_actual,
                    producto.marca,
                    producto.talla,
                    producto.id_categoria,
                    producto.id_producto
                )
            )

            conexion.commit()

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            raise error

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def eliminar(self, id_producto):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                raise Exception(
                    "No fue posible conectar con PostgreSQL"
                )

            cursor = conexion.cursor()

            cursor.execute(
                """
                DELETE FROM productos
                WHERE id_producto = %s
                """,
                (id_producto,)
            )

            conexion.commit()

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            raise error

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()