from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Primitivo import Primitivo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

class Unset(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        simbolo = ent.obtener(str(self.id)) 
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, El identificador "+str(self.id)+" no existe!!",self.linea,self.columna)
            ReporteErrores.func(error)
        else:

            if(self.id == "$ra" or self.id == "$sp"):
                error = Error("SEMANTICO","Error semantico, No es permitido eliminar la variable "+str(self.id)+" ya que es una variable del sistema!!",self.linea,self.columna)
                ReporteErrores.func(error)
                return None

            if(len(simbolo.punteros)>0):
                for var in simbolo.punteros:
                    simboloP = ent.obtener(str(var))
                    simboloP.valor = simbolo.valor
                    simboloP.puntero = ""
                    ent.reemplazar(simboloP)
                   
            ent.eliminar(str(self.id))