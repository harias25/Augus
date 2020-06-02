from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ast.Simbolo import TIPO_DATO as Tipo

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor

    def ejecutar(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        value = self.valor.getValorImplicito(ent,arbol) 
        if(simbolo == None):
            declarar = Declaracion(str(self.id),value,self.linea,self.columna)
            declarar.ejecutar(ent,arbol)
        else:
            simbolo.valor = value
            ent.reemplazar(simbolo)
        
    def getTipo(self,value):
        if(value == True or value == False):
            return Tipo.BOOLEAN
        elif isinstance(value, str):
            return Tipo.STRING
        elif isinstance(value, int):
            return Tipo.ENTERO
        elif isinstance(value, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL