from database.conexion import Conexion
from models.cliente import Cliente


class ClienteDAO:

    def obtener_clientes(self):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nombre,
                    telefono,
                    direccion,
                    correo
                FROM clientes
                ORDER BY id_cliente
            """)

            registros = cursor.fetchall()
            clientes = []

            for registro in registros:

                cliente = Cliente(
                    id_cliente=registro[0],
                    nombre=registro[1],
                    telefono=registro[2],
                    direccion=registro[3],
                    correo=registro[4]
                )

                clientes.append(cliente)

            cursor.close()
            conexion.close()

            return clientes

        except Exception as error:
            print("Error al consultar clientes:")
            print(error)

            return []

    def insertar(self, cliente):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO clientes(
                    nombre,
                    telefono,
                    direccion,
                    correo
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    cliente.nombre,
                    cliente.telefono,
                    cliente.direccion,
                    cliente.correo
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al registrar cliente:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def actualizar(self, cliente):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE clientes
                SET nombre = %s,
                    telefono = %s,
                    direccion = %s,
                    correo = %s
                WHERE id_cliente = %s
                """,
                (
                    cliente.nombre,
                    cliente.telefono,
                    cliente.direccion,
                    cliente.correo,
                    cliente.id_cliente
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al actualizar cliente:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def eliminar(self, id_cliente):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                DELETE FROM clientes
                WHERE id_cliente = %s
                """,
                (id_cliente,)
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al eliminar cliente:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()