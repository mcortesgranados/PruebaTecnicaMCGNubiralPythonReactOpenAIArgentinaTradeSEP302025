from datetime import date

class RegistroImportExport:
    def __init__(self, id_registro: int, fecha: date, operacion: str, clae2: str, clae3: str, clae6: str, letra: str, empresas: float, total_fob: float, total_cif: float):
        self.id_registro = id_registro
        self.fecha = fecha
        self.operacion = operacion
        self.clae2 = clae2
        self.clae3 = clae3
        self.clae6 = clae6
        self.letra = letra
        self.empresas = empresas
        self.total_fob = total_fob
        self.total_cif = total_cif