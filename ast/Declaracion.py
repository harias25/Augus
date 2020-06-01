from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo

class Declaracion(Instruccion):

    def __init__(self,id,tipo,valor,linea, columna):
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self,ent,arbol):
        #validar si existe el simbolo dentro de la tabla
        if(ent.existe(self.id)):
            print("El identificador "+self.id+" ya existe dentro de la tabla de Simbolos")
            return None
        #validar que no exista una función con el mismo nombre

        if self.valor != None:
            self.valor = self.valor.getValorImplicito(ent,arbol)
            tipoV = self.getTipo(self.valor)
            if(tipoV != self.tipo):

                print("Se está intentando asignar un valor "+str(tipoV.name)+" a una variable de tipo "+str(self.tipo.name))
                self.valor = None

        simbolo = Simbolo(self.id,self.tipo,self.valor,self.linea,self.columna)
        ent.agregar(simbolo)
    
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
