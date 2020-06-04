from datetime import datetime

class Error():
    def __init__(self,tipoError,descripcion,linea,columna):
        self.tipo = tipoError
        self.error = descripcion
        self.linea = str(linea)
        self.columna = str(columna)
        self.fechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        