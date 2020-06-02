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
    def __init__(self, id, valor,linea,columna,puntero) :
        self.id = id
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.punteros = [ ]
        self.puntero = puntero

    def getValorImplicito(self,ent,arbol):
        return self.valor

    def getTipo(self,ent,arbol):
        if isinstance(self.valor, str):
            return TIPO_DATO.STRING
        elif isinstance(self.valor, int):
            return TIPO_DATO.ENTERO
        elif isinstance(self.valor, float):
            return TIPO_DATO.DOOBLE
        else:
            return TIPO_DATO.NULL