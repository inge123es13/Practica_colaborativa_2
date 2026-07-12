import psycopg2

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="tienda_shecsper",  # <--- Cambiado al nombre real que tienes en pgAdmin
            user="postgres",
            password="141819",       # <--- Pon aquí tu contraseña de pgAdmin
            port="5432"
        )
        # Aseguramos codificación UTF-8
        conexion.set_client_encoding('UTF8')
        return conexion
    except Exception as e:
        print(f"Error crítico al conectar con la base de datos: {repr(e)}")
        return None