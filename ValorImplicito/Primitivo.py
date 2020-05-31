from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo

class Primitivo(Expresion):
    def __init__(self,valor,linea,columna):
        self.valor          = valor     #Object
        self.linea          = linea
        self.columna        = columna
    
    def getValorImplicito(self,ent,arbol):
        return self.valor
    
    def getTipo(self,ent,arbol):

        if isinstance(self.valor, int):
            return Tipo.ENTERO
        elif isinstance(self.valor, str):
            return Tipo.STRING
        elif isinstance(self.valor, bool):
            return Tipo.BOOLEAN
        elif isinstance(self.valor, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL
