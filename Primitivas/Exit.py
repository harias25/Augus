from ast.Instruccion import Instruccion

class Exit(Instruccion) :
    def __init__(self,linea,columna) :
        self.linea = linea
        self.columna = columna