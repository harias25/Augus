from ast.Instruccion import Instruccion
import ast.Entorno as TS

class If(Instruccion) :
    def __init__(self,  condicion, instruccionV,linea,columna) :
        self.condicion = condicion
        self.instruccionV = instruccionV
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        resultado = self.condicion.getValorImplicito(ent,arbol)
        if(resultado == 0 or resultado == 0.0): resultado = False
        if(resultado == 1 or resultado == 1.0): resultado = True

        if(not isinstance(resultado,bool)):
            print("Se esperaba un valor 1 o 0 para validar el IF.")

        if(bool(resultado)):
            self.instruccionV.ejecutar(ent,arbol)