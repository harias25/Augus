from enum import Enum
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo

class TIPO_OPERACION(Enum) :
    SUMA = 1
    RESTA= 2
    MULTIPLICACION= 3
    DIVISION= 4
    MODULO= 5
    POTENCIA= 6
    MENOS_UNARIO= 7
    MAYOR_QUE= 8
    MENOR_QUE= 9
    MAYOR_IGUA_QUE= 10
    MENOR_IGUA_QUE= 11
    IGUAL_IGUAL= 12
    DIFERENTE_QUE= 13
    PRIMITIVO= 14
    OR= 15
    AND= 16
    NOT= 17
    TERNARIO= 18

class Operacion(Expresion):
    def __init__(self):
        self.tipo           = None     #Tipo de Operacion
        self.ternario       = None     #Expresion Ternaria
        self.operadorIzq    = None     #Expresion
        self.operadorDer    = None     #Expresion
        self.valor          = None     #Object
        self.linea          = 0
        self.columna        = 0

    def Operacion(self,valor):
        self.tipo = TIPO_OPERACION.PRIMITIVO
        self.valor = valor


    def getValorImplicito(self,ent,arbol):
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.getValorImplicito(ent,arbol)


    def getTipo(self,ent,arbol):
        value = self.getValorImplicito(ent,arbol)
        if isinstance(value, int):
            return Tipo.ENTERO
        elif isinstance(value, str):
            return Tipo.STRING
        elif isinstance(value, bool):
            return Tipo.BOOLEAN
        elif isinstance(value, float):
            return Tipo.DOOBLE
        else:
            return Tipo.NULL

    