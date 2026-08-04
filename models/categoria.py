class Categoria:

    def __init__(
        self,
        id_categoria,
        nombre,
        descripcion
    ):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def mostrar_info(self):
        return (
            f"{self.id_categoria} - "
            f"{self.nombre} - "
            f"{self.descripcion}"
        )