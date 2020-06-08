from ast.Instruccion import Instruccion

class Exit(Instruccion) :
    def __init__(self,linea,columna) :
        pass

    def ejecutar(self,ent,arbol,ventana,isDebug):
        return True