class Usuario:

    def __init__(
        self,
        id_usuario,
        nombre,
        correo,
        contrasena,
        rol
    ):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def mostrar_info(self):
        return (
            f"{self.id_usuario} - "
            f"{self.nombre} - "
            f"{self.correo} - "
            f"Rol: {self.rol}"
        )