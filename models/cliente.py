class Cliente:

    def __init__(
        self,
        id_cliente,
        nombre,
        telefono,
        direccion,
        correo
    ):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

    def mostrar_info(self):
        return (
            f"{self.id_cliente} - "
            f"{self.nombre} - "
            f"{self.telefono} - "
            f"{self.correo}"
        )