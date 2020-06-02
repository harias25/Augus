from ast.Instruccion import Instruccion
import ast.Entorno as TS
import Primitivas.Exit as Exit

class GoTo(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        etiqueta = arbol.obtenerEtiqueta(self.id)

        if(etiqueta == None):
            print("No existe la etiqueta "+self.id)
        else:
            resultado = etiqueta.ejecutar(ent,arbol)
            if(type(resultado) is Exit.Exit): 
                return resultado   
            return True

        return False