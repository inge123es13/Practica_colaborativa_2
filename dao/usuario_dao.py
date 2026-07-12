from database.conexion import obtener_conexion
from models.usuario import Usuario

class UsuarioDAO:
    @staticmethod
    def listar_todos():
        conexion = obtener_conexion()
        if not conexion: return []
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_usuario, nombre, correo, contrasena, rol FROM usuarios ORDER BY id_usuario;")
            return [Usuario(f[0], f[1], f[2], f[3], f[4]) for f in cursor.fetchall()]
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def insertar(usuario):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s);",
                (usuario.nombre, usuario.correo, usuario.contrasena, usuario.rol)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(usuario):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, correo=%s, contrasena=%s, rol=%s WHERE id_usuario=%s;",
                (usuario.nombre, usuario.correo, usuario.contrasena, usuario.rol, usuario.id_usuario)
            )
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s;", (id_usuario,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario (verifica si tiene facturas asociadas): {e}")
            return False
        finally:
            cursor.close()
            conexion.close()