from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ast.Simbolo import TIPO_DATO as Tipo

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna,parametro):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.puntero = parametro

    def ejecutar(self,ent,arbol):

        simbolo = ent.obtener(str(self.id))
        value = {}
        if(not isinstance(self.valor,dict)):
            value = self.valor.getValorImplicito(ent,arbol) 

        if(self.puntero==False):
            if(simbolo == None):
                declarar = Declaracion(str(self.id),value,self.linea,self.columna,"")
                declarar.ejecutar(ent,arbol)
            else:
                if(simbolo.puntero != ""):
                    simboloP = ent.obtener(str(simbolo.puntero))
                    simboloP.valor = value
                    ent.reemplazar(simboloP)
                else:
                    simbolo.valor = value
                    ent.reemplazar(simbolo)
        else:
            if(value!=None):
                simboloP = ent.obtener(self.valor.valor)
                simboloP.punteros.append(self.id)
                if(simbolo == None):
                    declarar = Declaracion(str(self.id),self.valor,self.linea,self.columna,self.valor.valor)
                    declarar.ejecutar(ent,arbol)
                else:
                    simbolo.valor = self.valor
                    ent.reemplazar(simbolo)


    def getTipo(self,value):
        if isinstance(value, str):
            return Tipo.STRING
        elif isinstance(value, int):
            return Tipo.ENTERO
        elif isinstance(value, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL