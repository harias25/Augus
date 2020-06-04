
class AST:
    def __init__(self,instrucciones):
        self.instrucciones = instrucciones
        self.etiquetas = []

    def existeEtiqueta(self,id):
        for etiqueta in self.etiquetas:
            comparacion = etiqueta.id == id.id
            if(comparacion):
                return True

        return False
    
    def agregarEtiqueta(self,etiqueta):
        self.etiquetas.append(etiqueta)

    def obtenerEtiqueta(self,texto):
        for etiqueta in self.etiquetas:
            if(etiqueta.id == texto):
                return etiqueta

        return None

    def obtenerSiguienteEtiqueta(self,texto):
        contador = 0
        for etiqueta in self.etiquetas:
            if(etiqueta.id == texto):
                if(len(self.etiquetas) > (contador+1)):
                 return self.etiquetas[contador+1]
            contador = contador +1

        return None