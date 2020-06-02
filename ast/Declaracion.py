from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo

class Declaracion(Instruccion):

    def __init__(self,id,valor,linea, columna,puntero):
        self.id = id
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.puntero = puntero
    
    def ejecutar(self,ent,arbol):
        #validar si existe el simbolo dentro de la tabla
        if(ent.existe(self.id)):
            print("El identificador "+self.id+" ya existe dentro de la tabla de Simbolos")
            return None
        #validar que no exista una función con el mismo nombre
        simbolo = Simbolo(self.id,self.valor,self.linea,self.columna,self.puntero)
        ent.agregar(simbolo)
    
    def getTipo(self,value):
        if isinstance(value, str):
            return Tipo.STRING
        elif isinstance(value, int):
            return Tipo.ENTERO
        elif isinstance(value, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL
