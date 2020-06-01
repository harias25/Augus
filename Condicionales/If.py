from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Transferencia.Break import Break
from Transferencia.Continue import Continue
from Transferencia.Return import Return

class If(Instruccion) :
    def __init__(self,  condicion, instruccionesV, instruccionesF, lista_elseif,linea,columna) :
        self.condicion = condicion
        self.listaInstrucciones = instruccionesV
        self.listaInsElse = instruccionesF
        self.listadoElseIf = lista_elseif
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        resultado = self.condicion.getValorImplicito(ent,arbol)
        if(not isinstance(resultado,bool)):
            print("Se esperaba un valor de tipo booleano para validar el IF.")

        if(bool(resultado)):
            tablaLocal = TS.Entorno(ent)
            for ins in self.listaInstrucciones:
                if isinstance(ins,Break) or isinstance(ins,Continue):
                    return ins
                elif isinstance(ins,Return):
                    return ins.ejecutar(tablaLocal,arbol)

                ins.ejecutar(tablaLocal,arbol)
