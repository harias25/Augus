from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import Pantalla

class Imprimir(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

    def ejecutar(self,ent,arbol):
        valor = self.cad.getValorImplicito(ent,arbol)
        if(isinstance(valor,dict)):
            error = Error("SEMANTICO","Error semantico, no es posible imprimir un Array!!",0,1)
            ReporteErrores.func(error)
        elif(valor == None):
            return False
        else:
            print('> ', valor)
            Pantalla.getUI().setText(valor)