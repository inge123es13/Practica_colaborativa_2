class Usuario:
    def __init__(self, id_usuario=None, nombre="", correo="", contrasena="", rol=""):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol