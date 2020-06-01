from ast.Instruccion import Instruccion
from ast.Expresion import Expresion

class Return(Instruccion,Expresion) :
    def __init__(self,valor, linea,columna) :
        self.linea = linea
        self.columna = columna
        self.ValorRetorno = valor

    def getTipo(self,ent,arbol):
        return None

    def getValorImplicito(self,ent,arbol):
        if self.ValorRetorno!=None:
            return self.ValorRetorno.getValorImplicito(ent,arbol)
        else:
            return None
    
    def ejecutar(self,ent,arbol):
        return self.getValorImplicito(ent,arbol)