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
    ID = 19
    XOR = 20

class Operacion(Expresion):
    def __init__(self):
        self.tipo           = None     #Tipo de Operacion
        self.ternario       = None     #Expresion Ternaria
        self.operadorIzq    = None     #Expresion
        self.operadorDer    = None     #Expresion
        self.valor          = None     #Object
        self.linea          = 0
        self.columna        = 0

    def Primitivo(self,valor):
        self.tipo = TIPO_OPERACION.PRIMITIVO
        self.valor = valor

    def Indentficador(self,valor,linea,columna):
        self.tipo = TIPO_OPERACION.ID 
        self.valor = valor

    def Operacion(self,izq,der,operacion,linea,columna):
        self.tipo = operacion
        self.operadorIzq = izq
        self.operadorDer = der
        self.linea = linea
        self.columna = columna 

    def OperacionUnaria(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.MENOS_UNARIO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def OperacionNot(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.NOT
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna
    
    def obtenerValorNumerico(self,cadena):
        decimal = False
        retorno = ""
        for caracter in cadena:
            if(caracter.isdigit()):
                retorno +=caracter
            elif(caracter == "." and retorno!= ""):
                if not decimal:
                    decimal = True
                    retorno +=caracter
                else:
                    print("Error convirtiendo la cadena!!")
                    break
            else:
                print("Error convirtiendo la cadena!!")
                break
                
        if(retorno==""): return 0
        if retorno.endswith("."): return int(retorno[0:len(retorno)-1])
        if decimal : return float(retorno)

        return int(retorno)

    def getValorImplicito(self,ent,arbol):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.getValorImplicito(ent,arbol)

        #IDENTIFICADORES
        elif(self.tipo == TIPO_OPERACION.ID):
            simbolo = ent.obtener(str(self.valor))
            if(simbolo == None):
                print("No existe la variable "+str(self.valor))
                return None
            
            return simbolo.getValorImplicito(ent,arbol)

        #SUMA
        elif(self.tipo == TIPO_OPERACION.SUMA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(valor1) + int(valor2)
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return round(float(float(valor1) + float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return round(float(float(valor1) + float(valor2)),2)
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return round(float(float(valor1) + float(valor2)),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una SUMA")
                return None
        
        #RESTA
        elif(self.tipo == TIPO_OPERACION.RESTA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)
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
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)
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
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

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
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

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
        elif(self.tipo == TIPO_OPERACION.MENOS_UNARIO):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            #OPERACION DE ENTEROS
            if isinstance(valor1, int):
                return int(valor1) * -1 
            elif isinstance(valor1, float):     # FLOAT
                return round(float(float(valor1) * -1),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipo de dato permitido para el operador UNARIO")
                return None
        
        #MAYOR
        elif(self.tipo == TIPO_OPERACION.MAYOR_QUE):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) > int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int(float(valor1) > float(valor2))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int(float(valor1) > float(valor2))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int(float(valor1) > float(valor2))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                if sinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) > valor2)
                elif sinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 > len(str(valor2)))
                return int(len(str(valor1)) > len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>' ")
                return None
        
        #MAYOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MAYOR_IGUA_QUE):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) >= int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int(float(valor1) >= float(valor2))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int(float(valor1) >= float(valor2))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int(float(valor1) >= float(valor2))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                if sinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) >= valor2)
                elif sinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 >= len(str(valor2)))
                return int(len(str(valor1)) >= len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>=' ")
                return None

        #MENOR
        elif(self.tipo == TIPO_OPERACION.MENOR_QUE):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) < int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int((float(valor1) < float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int((float(valor1) < float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int((float(valor1) < float(valor2)))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                if sinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) < valor2)
                elif sinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 < len(str(valor2)))
                return int(len(str(valor1)) < len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>' ")
                return None
        
        #MENOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MENOR_IGUA_QUE):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) <= int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int((float(valor1) <= float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int((float(valor1) <= float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int((float(valor1) <= float(valor2)))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                if sinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) <= valor2)
                elif sinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 <= len(str(valor2)) )
                return int(len(str(valor1)) <= len(str(valor2)) ) 
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>=' ")
                return None

        #IGUAL
        elif(self.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) == int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int((float(valor1) == float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int((float(valor1) == float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int((float(valor1) == float(valor2)))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                return int(str(valor1) == str(valor2) )
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>' ")
                return None
        
        #DIFERENTE
        elif(self.tipo == TIPO_OPERACION.DIFERENTE_QUE):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            
            #OPERACION DE ENTEROS
            if isinstance(valor1, int) and isinstance(valor2, int):
                return int(int(valor1) != int(valor2))
            elif isinstance(valor1, int) and isinstance(valor2, float):     # ENTERO - FLOAT
                return int((float(valor1) != float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, int):     # FLOAT - ENTERO
                return int((float(valor1) != float(valor2)))
            elif isinstance(valor1, float) and isinstance(valor2, float):   # FLOAT - FLOAT
                return int((float(valor1) != float(valor2)))
            elif isinstance(valor1, str) or isinstance(valor2, str):        # CONCATENACIÓN STRINGS
                if valor1 == None : valor1 = ""
                if valor2 == None : valor2 = ""
                return int(str(valor1) != str(valor2))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion relacional '>=' ")
                return None

        #AND
        elif(self.tipo == TIPO_OPERACION.AND):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(valor1 == 0 or valor1 == 0.0): valor1 = False
            if(valor1 == 1 or valor1 == 1.0): valor1 = True

            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(valor2 == 0 or valor2 == 0.0): valor2 = False
            if(valor2 == 1 or valor2 == 1.0): valor2 = True

            if isinstance(valor1, bool) and isinstance(valor2, bool):
                return int(bool(valor1) and bool(valor2))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion logica AND ")
                return None

        #OR
        elif(self.tipo == TIPO_OPERACION.OR):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(valor1 == 0 or valor1 == 0.0): valor1 = False
            if(valor1 == 1 or valor1 == 1.0): valor1 = True

            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(valor2 == 0 or valor2 == 0.0): valor2 = False
            if(valor2 == 1 or valor2 == 1.0): valor2 = True

            if isinstance(valor1, bool) and isinstance(valor2, bool):
                return int(bool(valor1) or bool(valor2))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion logica OR ")
                return None

        #XOR
        elif(self.tipo == TIPO_OPERACION.XOR):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(valor1 == 0 or valor1 == 0.0): valor1 = False
            if(valor1 == 1 or valor1 == 1.0): valor1 = True

            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(valor2 == 0 or valor2 == 0.0): valor2 = False
            if(valor2 == 1 or valor2 == 1.0): valor2 = True

            if isinstance(valor1, bool) and isinstance(valor2, bool):
                return int(bool(valor1) ^ bool(valor2))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion logica XOR ")
                return None

        #NOT
        elif(self.tipo == TIPO_OPERACION.NOT):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(valor1 == 0 or valor1 == 0.0): valor1 = False
            if(valor1 == 1 or valor1 == 1.0): valor1 = True

            if isinstance(valor1, bool):
                return int(not bool(valor1))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                print("Error en tipos de datos permitidos para una expresion logica NOT ")
                return None
        

    def getTipo(self,ent,arbol):
        value = self.getValorImplicito(ent,arbol)
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

    