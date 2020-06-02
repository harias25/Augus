from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Primitivo import Primitivo
class Unset(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        simbolo = ent.obtener(str(self.id)) 
        if(simbolo == None):
            print("El identificador "+str(self.id)+" no existe!!")
        else:

            if(self.id == "$ra" or self.id == "$sp"):
                print("No es permitido eliminar la variable "+str(self.id)+" ya que es una variable del sistema!!")
                return None

            if(len(simbolo.punteros)>0):
                for var in simbolo.punteros:
                    simboloP = ent.obtener(str(var))
                    simboloP.valor = simbolo.valor
                    simboloP.puntero = ""
                    ent.reemplazar(simboloP)
                   
            ent.eliminar(str(self.id))