class Material:
    def __init__(self, id: str, nombre_material: str, tipo_material: str,
                 renovable: bool, reciclable: bool, impacto_ambiental: str,
                 imagen_url: str):
        self.id = id
        self.nombre_material = nombre_material
        self.tipo_material = tipo_material
        self.renovable = renovable
        self.reciclable = reciclable
        self.impacto_ambiental = impacto_ambiental
        self.imagen_url = imagen_url
