from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ValorImplicito.Primitivo import Primitivo
from ValorImplicito.Asignacion import Asignacion
from ast.Simbolo import TIPO_DATO as Tipo
import Reporteria.Error as Error
import Reporteria.ReporteErrores as ReporteErrores

class Conversion(Instruccion):
    def __init__(self,id,valor,tipo,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.declarada = None

    def setAmbito(self,ambito):
        self.declarada = ambito

    def ejecutar(self,ent,arbol,ventana,isDebug):
        value = self.valor.getValorImplicito(ent,arbol) 

        if(isinstance(value,dict)):
            els = list(value.items())
            value = els[0][1]

        if(isinstance(value,dict)):
            error = Error.Error("SEMANTICO","Error semantico, La primera posición del array es otro array. ",self.linea,self.columna)
            ReporteErrores.func(error)
            return False

        if(self.tipo == 'int'):
            if(isinstance(value,float)):
                value = int(value)
            elif(isinstance(value,str)):
                value = ord(value[0])
            else: 
                value = value

        elif(self.tipo == 'float'):
            if(isinstance(value,int)):
                value = float(value)
            elif(isinstance(value,str)):
                value = float(ord(value[0]))
            else:
                value = value
        else:
            if(isinstance(value,float)):  value = int(value)
            if(isinstance(value,int)):
                if(value >255): value = value - 256
                value = chr(value)
            elif(isinstance(value,str)):
                value = value[0]
            else:
                value = value

        
        primitivo = Primitivo(value,self.linea,self.columna)
        asignacion = Asignacion(self.id,primitivo,self.linea,self.columna,False)
        asignacion.setAmbito(self.declarada)
        asignacion.ejecutar(ent,arbol,ventana,isDebug)

        return False
