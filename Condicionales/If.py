from ast.Instruccion import Instruccion
import ast.Entorno as TS

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
                ins.ejecutar(tablaLocal,arbol)
