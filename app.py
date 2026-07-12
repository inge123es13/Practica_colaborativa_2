import sys
from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria
from dao.producto_dao import ProductoDAO
from models.producto import Producto
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

def menu_categorias():
    while True:
        print("\n=== MÓDULO CATEGORÍAS ===")
        print("1. Visualizar Categorías")
        print("2. Agregar Categoría")
        print("3. Editar Categoría")
        print("4. Eliminar Categoría")
        print("5. Volver al menú principal")
        opc = input("Selecciona una opción: ")

        if opc == "1":
            cats = CategoriaDAO.listar_todas()
            print("\n--- LISTADO DE CATEGORÍAS ---")
            for c in cats:
                print(f"[{c.id_categoria}] {c.nombre} - {c.descripcion}")
        elif opc == "2":
            nom = input("Nombre: ")
            desc = input("Descripción: ")
            if CategoriaDAO.insertar(Categoria(nombre=nom, descripcion=desc)):
                print("¡Categoría guardada con éxito!")
            else:
                print("Error al guardar.")
        elif opc == "3":
            id_cat = input("ID de la categoría a editar: ")
            nom = input("Nuevo Nombre: ")
            desc = input("Nueva Descripción: ")
            if CategoriaDAO.actualizar(Categoria(id_categoria=int(id_cat), nombre=nom, descripcion=desc)):
                print("¡Categoría modificada con éxito!")
            else:
                print("No se pudo actualizar (Verifica el ID).")
        elif opc == "4":
            id_cat = input("ID de la categoría a eliminar: ")
            if CategoriaDAO.eliminar(int(id_cat)):
                print("¡Categoría eliminada!")
            else:
                print("No se pudo eliminar.")
        elif opc == "5":
            break

def menu_productos():
    while True:
        print("\n=== MÓDULO PRODUCTOS ===")
        print("1. Visualizar Productos")
        print("2. Agregar Producto")
        print("3. Editar Producto")
        print("4. Eliminar Producto")
        print("5. Volver al menú principal")
        opc = input("Selecciona una opción: ")

        if opc == "1":
            prods = ProductoDAO.listar_todos()
            print("\n--- LISTADO DE PRODUCTOS ---")
            for p in prods:
                print(f"[{p.id_producto}] {p.nombre} | Marca: {p.marca} | Talla: {p.talla} | Precio: ${p.precio} | Stock: {p.stock_actual} | Cat ID: {p.id_categoria}")
        elif opc == "2":
            nom = input("Nombre: ")
            desc = input("Descripción: ")
            prec = float(input("Precio: "))
            stock = int(input("Stock Inicial: "))
            marca = input("Marca: ")
            talla = input("Talla: ")
            id_cat = int(input("ID de Categoría Asignada: "))
            
            nuevo_p = Producto(nombre=nom, descripcion=desc, precio=prec, stock_actual=stock, marca=marca, talla=talla, id_categoria=id_cat)
            if ProductoDAO.insertar(nuevo_p):
                print("¡Producto agregado al inventario!")
            else:
                print("Error al insertar producto.")
        elif opc == "3":
            id_prod = int(input("ID del producto a editar: "))
            nom = input("Nuevo Nombre: ")
            desc = input("Nueva Descripción: ")
            prec = float(input("Nuevo Precio: "))
            stock = int(input("Nuevo Stock: "))
            marca = input("Nueva Marca: ")
            talla = input("Nueva Talla: ")
            id_cat = int(input("Nuevo ID de Categoría: "))
            
            p_editado = Producto(id_producto=id_prod, nombre=nom, descripcion=desc, precio=prec, stock_actual=stock, marca=marca, talla=talla, id_categoria=id_cat)
            if ProductoDAO.actualizar(p_editado):
                print("¡Producto modificado!")
            else:
                print("Error al actualizar.")
        elif opc == "4":
            id_prod = int(input("ID del producto a eliminar: "))
            if ProductoDAO.eliminar(id_prod):
                print("¡Producto eliminado del inventario!")
            else:
                print("No se pudo eliminar.")
        elif opc == "5":
            break

def menu_usuarios():
    while True:
        print("\n=== MÓDULO USUARIOS ===")
        print("1. Visualizar Usuarios")
        print("2. Agregar Usuario")
        print("3. Editar Usuario")
        print("4. Eliminar Usuario")
        print("5. Volver al menú principal")
        opc = input("Selecciona una opción: ")

        if opc == "1":
            users = UsuarioDAO.listar_todos()
            print("\n--- LISTADO DE USUARIOS ---")
            for u in users:
                print(f"[{u.id_usuario}] {u.nombre} | Correo: {u.correo} | Rol: {u.rol}")
        elif opc == "2":
            nom = input("Nombre completo: ")
            correo = input("Correo electrónico: ")
            contra = input("Contraseña: ")
            rol = input("Rol (Admin/Empleado/Cliente): ")
            
            nuevo_u = Usuario(nombre=nom, correo=correo, contrasena=contra, rol=rol)
            if UsuarioDAO.insertar(nuevo_u):
                print("¡Usuario registrado con éxito!")
            else:
                print("Error al registrar usuario.")
        elif opc == "3":
            id_user = int(input("ID del usuario a editar: "))
            nom = input("Nuevo Nombre: ")
            correo = input("Nuevo Correo: ")
            contra = input("Nueva Contraseña: ")
            rol = input("Nuevo Rol: ")
            
            u_editado = Usuario(id_usuario=id_user, nombre=nom, correo=correo, contrasena=contra, rol=rol)
            if UsuarioDAO.actualizar(u_editado):
                print("¡Datos de usuario actualizados!")
            else:
                print("Error al actualizar el usuario.")
        elif opc == "4":
            id_user = int(input("ID del usuario a eliminar: "))
            if UsuarioDAO.eliminar(id_user):
                print("¡Usuario eliminado correctamente!")
            else:
                print("No se pudo eliminar el usuario.")
        elif opc == "5":
            break

def menu_principal():
    while True:
        print("\n======================================")
        print("   SISTEMA DE GESTIÓN DE INVENTARIO")
        print("======================================")
        print("1. Administrar Categorías")
        print("2. Administrar Productos")
        print("3. Administrar Usuarios")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_categorias()
        elif opcion == "2":
            menu_productos()
        elif opcion == "3":
            menu_usuarios()
        elif opcion == "4":
            print("Cerrando aplicación...")
            sys.exit()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()