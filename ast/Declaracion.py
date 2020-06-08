from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo

class Declaracion(Instruccion):

    def __init__(self,id,valor,linea, columna,puntero,declarada):
        self.id = id
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.puntero = puntero
        self.declarada = declarada
    
    def ejecutar(self,ent,arbol,ventana,isDebug):
        #validar si existe el simbolo dentro de la tabla
        simbolo = Simbolo(self.id,self.valor,self.linea,self.columna,self.puntero,self.declarada)

        if(ent.existe(self.id)):
            ent.reemplazar(simbolo)
        else:
            ent.agregar(simbolo)
        
        return False
