from database.conexion import obtener_conexion
from models.categoria import Categoria

class CategoriaDAO:
    @staticmethod
    def listar_todas():
        conexion = obtener_conexion()
        if not conexion: return []
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_categoria, nombre, descripcion FROM categorias ORDER BY id_categoria;")
            return [Categoria(f[0], f[1], f[2]) for f in cursor.fetchall()]
        except Exception as e:
            print(f"Error al listar categorías: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def insertar(categoria):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s);", (categoria.nombre, categoria.descripcion))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar categoría: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(categoria):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE categorias SET nombre=%s, descripcion=%s WHERE id_categoria=%s;", (categoria.nombre, categoria.descripcion, categoria.id_categoria))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar categoría: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_categoria):
        conexion = obtener_conexion()
        if not conexion: return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id_categoria=%s;", (id_categoria,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar categoría (verifica dependencias): {e}")
            return False
        finally:
            cursor.close()
            conexion.close()