from ast.Instruccion import Instruccion

class Continue(Instruccion) :
    def __init__(self,  linea,columna) :
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        return self