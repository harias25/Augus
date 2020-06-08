from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
                        
class Imprimir(Instruccion) :
    def __init__(self,cad,linea,columna):
        self.cad = cad
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        valor = self.cad.getValorImplicito(ent,arbol)
        if(isinstance(valor,dict)):
            error = Error("SEMANTICO","Error semantico, no es posible imprimir un Array!!",0,1)
            ReporteErrores.func(error)
        elif(valor == None):
            return False
        else:
            print('> ', valor)