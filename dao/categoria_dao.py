from database.conexion import Conexion
from models.categoria import Categoria


class CategoriaDAO:

    def obtener_categorias(self):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_categoria,
                    nombre,
                    descripcion
                FROM categorias
                ORDER BY id_categoria
            """)

            registros = cursor.fetchall()
            categorias = []

            for registro in registros:

                categoria = Categoria(
                    id_categoria=registro[0],
                    nombre=registro[1],
                    descripcion=registro[2]
                )

                categorias.append(categoria)

            cursor.close()
            conexion.close()

            return categorias

        except Exception as error:
            print("Error al consultar las categorías:")
            print(error)

            return []

    def insertar(self, categoria):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO categorias(
                    nombre,
                    descripcion
                )
                VALUES (%s, %s)
                """,
                (
                    categoria.nombre,
                    categoria.descripcion
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al registrar la categoría:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def actualizar(self, categoria):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE categorias
                SET nombre = %s,
                    descripcion = %s
                WHERE id_categoria = %s
                """,
                (
                    categoria.nombre,
                    categoria.descripcion,
                    categoria.id_categoria
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al actualizar la categoría:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()