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

    def OperacionAritmetica(self,izq,der,operacion,linea,columna):
        self.tipo = operacion
        self.operadorIzq = izq
        self.operadorDer = der
        self.linea = linea
        self.columna = columna


    def getValorImplicito(self,ent,arbol):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.getValorImplicito(ent,arbol)
        
        #SUMA
        elif(self.tipo == TIPO_OPERACION.SUMA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) + int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) + float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) + float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) + float(valor2)),2)
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                return str(valor1) + str(valor2) 
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una SUMA")
                return None
        
        #RESTA
        elif(self.tipo == TIPO_OPERACION.RESTA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) - int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) - float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) - float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) - float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una RESTA")
                return None

        #MULTIPLICACIÓN
        elif(self.tipo == TIPO_OPERACION.MULTIPLICACION):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) * int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) * float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) * float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) * float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una MULTIPLICACIÓN")
                return None
        
        #DIVISION
        elif(self.tipo == TIPO_OPERACION.DIVISION):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            if(isinstance(valor2, int) or  isinstance(valor2, float)):
                temp = int(valor2)
                if(temp == 0):
                    print("No es posible una DIVISION sobre CERO")
                    return None

            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) / int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) / float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) / float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) / float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una DIVISION")
                return None

        #MODULO
        elif(self.tipo == TIPO_OPERACION.MODULO):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            if(isinstance(valor2, int) or  isinstance(valor2, float)):
                temp = int(valor2)
                if(temp == 0):
                    print("No es posible un MODULO sobre CERO")
                    return None

            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) % int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) % float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) % float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) % float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para un MODULO")
                return None

        #POTENCIA
        elif(self.tipo == TIPO_OPERACION.POTENCIA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) ** int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) ** float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) ** float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) ** float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una POTENCIA")
                return None

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

    