from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
                        
class Imprimir(Instruccion) :
    def __init__(self,cad,linea,columna):
        self.cad = cad
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        valor = self.cad.getValorImplicito(ent,arbol)
        if(isinstance(valor,dict)):
            error = Error("SEMANTICO","Error semantico, no es posible imprimir un Array!!",self.linea,self.columna)
            ReporteErrores.func(error)
        elif(valor == None):
            return False
        elif(str(valor) == "\n"):
            print('> ', "")
            ventana.consola.appendPlainText("")
        else:
            print('> ', valor)
            cadenas = str(valor).split("\\n")
            
            if(len(cadenas) == 1):
                 ventana.consola.insertPlainText(str(valor))
            else:
                contador = 1
                for value in cadenas:
                    ventana.consola.insertPlainText(str(value))
                    if(contador < len(cadenas)):
                        ventana.consola.appendPlainText("")
                    contador = contador + 1

           