from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ValorImplicito.Primitivo import Primitivo
from ValorImplicito.Asignacion import Asignacion
from ast.Simbolo import TIPO_DATO as Tipo

class Conversion(Instruccion):
    def __init__(self,id,valor,tipo,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.tipo = tipo

    def ejecutar(self,ent,arbol):
        value = self.valor.getValorImplicito(ent,arbol) 
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
        asignacion.ejecutar(ent,arbol)
