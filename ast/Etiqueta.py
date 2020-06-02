from ast.Instruccion import Instruccion
import ast.Entorno as TS
import Primitivas.Exit as Exit

class Etiqueta(Instruccion) :
    def __init__(self,  id, instrucciones,linea,columna) :
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        for ins in self.instrucciones:
            if(type(ins) is Exit.Exit): 
                return ins

            ins.ejecutar(ent,arbol)
        
        siguiente = arbol.obtenerSiguienteEtiqueta(self.id)
        if(siguiente!=None):
            siguiente.ejecutar(ent,arbol)

        return None
