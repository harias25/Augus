#Clase principal para el manejo de los simbolos que soportará el programa

from enum import Enum
from ast.Expresion import Expresion

class TIPO_DATO(Enum) :
    ENTERO = 1,
    DOOBLE = 2,
    STRING = 3,
    BOOLEAN = 4,
    NULL = 5

class Simbolo(Expresion) :
    def __init__(self, id, tipo, valor,linea,columna) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

        if(valor == None):
            if(self.tipo == TIPO_DATO.ENTERO):
                self.valor = 0
            elif(self.tipo == TIPO_DATO.DOOBLE):
                self.valor = 0.0
            elif(self.tipo == TIPO_DATO.BOOLEAN):
                self.valor = False
            else:
                self.valor = ""

    def getValorImplicito(self,ent,arbol):
        return self.valor

    def getTipo(self,ent,arbol):
        return self.tipo