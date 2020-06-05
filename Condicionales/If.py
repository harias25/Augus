from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import Primitivas.Exit as Exit

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
            error = Error("SEMANTICO","Error semantico, Se esperaba un valor 1 o 0 para validar el IF.",self.linea,self.columna)
            ReporteErrores.func(error)

        if(bool(resultado)):
            try:
                ins_result = self.instruccionV.ejecutar(ent,arbol)
                #if(isinstance(ins_result),Exit): return ins_result
                return True
            except:
                return False

        return False
        