from ast.Instruccion import Instruccion
import ast.Entorno as TS
import Primitivas.Exit as Exit
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
#import pruebas

class GoTo(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        etiqueta = arbol.obtenerEtiqueta(self.id)

        if(etiqueta == None):
            error = Error("SEMANTICO","Error semantico, no existe la etiqueta "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
        else:
            resultado = etiqueta.ejecutar(ent,arbol)
            if(type(resultado) is Exit.Exit): 
                return resultado   
            return True

        return False