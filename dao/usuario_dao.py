from database.conexion import Conexion
from models.usuario import Usuario


class UsuarioDAO:

    def obtener_usuarios(self):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    correo,
                    contrasena,
                    rol
                FROM usuarios
                ORDER BY id_usuario
            """)

            registros = cursor.fetchall()
            usuarios = []

            for registro in registros:

                usuario = Usuario(
                    id_usuario=registro[0],
                    nombre=registro[1],
                    correo=registro[2],
                    contrasena=registro[3],
                    rol=registro[4]
                )

                usuarios.append(usuario)

            cursor.close()
            conexion.close()

            return usuarios

        except Exception as error:
            print("Error al consultar usuarios:")
            print(error)

            return []

    def insertar(self, usuario):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios(
                    nombre,
                    correo,
                    contrasena,
                    rol
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    usuario.nombre,
                    usuario.correo,
                    usuario.contrasena,
                    usuario.rol
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al registrar usuario:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def actualizar(self, usuario):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE usuarios
                SET nombre = %s,
                    correo = %s,
                    contrasena = %s,
                    rol = %s
                WHERE id_usuario = %s
                """,
                (
                    usuario.nombre,
                    usuario.correo,
                    usuario.contrasena,
                    usuario.rol,
                    usuario.id_usuario
                )
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al actualizar usuario:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def eliminar(self, id_usuario):

        conexion = None
        cursor = None

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )

            conexion.commit()

            return True

        except Exception as error:

            if conexion is not None:
                conexion.rollback()

            print("Error al eliminar usuario:")
            print(error)

            return False

        finally:

            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def autenticar(self, correo, contrasena):

        try:
            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT
                    id_usuario,
                    nombre,
                    correo,
                    contrasena,
                    rol
                FROM usuarios
                WHERE correo = %s
                  AND contrasena = %s
                """,
                (
                    correo,
                    contrasena
                )
            )

            registro = cursor.fetchone()

            cursor.close()
            conexion.close()

            if registro is None:
                return None

            return Usuario(
                id_usuario=registro[0],
                nombre=registro[1],
                correo=registro[2],
                contrasena=registro[3],
                rol=registro[4]
            )

        except Exception as error:
            print("Error al iniciar sesión:")
            print(error)

            return None