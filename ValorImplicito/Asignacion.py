from ast.Instruccion import Instruccion
from ast.Simbolo import TIPO_DATO as Tipo

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor

    def ejecutar(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            print("No existe la variable "+str(self.id))
            return None
        else:
            value = self.valor.getValorImplicito(ent,arbol) 
            tipo = self.getTipo(value)

            if(tipo==simbolo.tipo):
                simbolo.valor = value
                ent.reemplazar(simbolo)
            else:
                print("Se está intentando asignar un valor "+str(tipo.name)+" a una variable de tipo "+str(simbolo.tipo.name))

    def getTipo(self,value):
        if(value == True or value == False):
            return Tipo.BOOLEAN
        elif isinstance(value, str):
            return Tipo.STRING
        elif isinstance(value, int):
            return Tipo.ENTERO
        elif isinstance(value, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL