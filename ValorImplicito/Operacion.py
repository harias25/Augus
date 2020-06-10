from enum import Enum
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

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
    ABSOLUTO = 21
    NOTR = 22
    PAND = 23
    BOR = 24
    XORR = 25
    SHIFTI = 26
    SHIFTD = 27
    ACCESO = 28

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

    def ValorAbsoluto(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.ABSOLUTO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def AccesoLista(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.ACCESO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def OperacionNot(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.NOT
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def OperacionNotBit(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.NOTR
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
                    error = Error("SEMANTICO","Error semantico, No es posible convertir la cadena ("+cadena+") a un número",self.linea,self.columna)
                    ReporteErrores.func(error)
                    break
            else:
                error = Error("SEMANTICO","Error semantico, No es posible convertir la cadena ("+cadena+") a un número",self.linea,self.columna)
                ReporteErrores.func(error)
                break
                
        if(retorno==""): return 0
        if retorno.endswith("."): return int(retorno[0:len(retorno)-1])
        if decimal : return float(retorno)

        return int(retorno)

    def getValorImplicito(self,ent,arbol):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.getValorImplicito(ent,arbol)

        #ACCESOS LISTAS
        elif(self.tipo == TIPO_OPERACION.ACCESO):
            return self.operadorIzq.getValorImplicito(ent,arbol)
        #IDENTIFICADORES
        elif(self.tipo == TIPO_OPERACION.ID):
            simbolo = ent.obtener(str(self.valor))
            if(simbolo == None):
                error = Error("SEMANTICO","Error semantico, No es existe la variable "+str(self.valor),self.linea,self.columna)
                ReporteErrores.func(error)
                return None
            
            valorRetorno = simbolo.getValorImplicito(ent,arbol)
            if(type(valorRetorno) is Operacion ): 
                return valorRetorno.getValorImplicito(ent,arbol)
            return valorRetorno

        #SUMA
        elif(self.tipo == TIPO_OPERACION.SUMA):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)

            #concatenación de strings
            if(isinstance(valor1,str) and isinstance(valor2,str)):
                return valor1 + valor2

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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una SUMA",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una RESTA",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una MULTIPLICACION",self.linea,self.columna)
                ReporteErrores.func(error)
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
                    error = Error("SEMANTICO","Error semantico, No es posible una división sobre CERO!",self.linea,self.columna)
                    ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una DIVISION",self.linea,self.columna)
                ReporteErrores.func(error)
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
                    error = Error("SEMANTICO","Error semantico, No es posible una modulo sobre CERO!",self.linea,self.columna)
                    ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una MODULO",self.linea,self.columna)
                ReporteErrores.func(error)
                return None

        #UNARIA
        elif(self.tipo == TIPO_OPERACION.MENOS_UNARIO):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)

            #OPERACION DE ENTEROS
            if isinstance(valor1, int):
                return int(valor1) * -1 
            elif isinstance(valor1, float):     # FLOAT
                return round(float(float(valor1) * -1),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipo de dato permitido para un UNARIO",self.linea,self.columna)
                ReporteErrores.func(error)
                return None
        
        #ABSOLUTO
        elif(self.tipo == TIPO_OPERACION.ABSOLUTO):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)

            #OPERACION DE ENTEROS
            if isinstance(valor1, int):
                return abs(int(valor1)) 
            elif isinstance(valor1, float):     # FLOAT
                return round(abs(float(float(valor1))),2)
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipo de dato permitido para un VALOR ABSOLUTO",self.linea,self.columna)
                ReporteErrores.func(error)
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
                if isinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) > valor2)
                elif isinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 > len(str(valor2)))
                return int(len(str(valor1)) > len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '>' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                if isinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) >= valor2)
                elif isinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 >= len(str(valor2)))
                return int(len(str(valor1)) >= len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '>=' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                if isinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) < valor2)
                elif isinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 < len(str(valor2)))
                return int(len(str(valor1)) < len(str(valor2)))
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '<' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                if isinstance(valor1, str) and not isinstance(valor2, str):
                    return int(len(str(valor1)) <= valor2)
                elif isinstance(valor2, str) and not isinstance(valor1, str):
                    return int(valor1 <= len(str(valor2)) )
                return int(len(str(valor1)) <= len(str(valor2)) ) 
            else:
                #ERROR DE TIPOS DE DATOS PERMITIDOS PARA LA OPERACION
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '<=' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '==' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion relacional '!=' ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion logica AND ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion logica OR ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipos de datos permitidos para una expresion logica XOR ",self.linea,self.columna)
                ReporteErrores.func(error)
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
                error = Error("SEMANTICO","Error semantico, Error en tipo de dato permitido para una expresion logica NOT ",self.linea,self.columna)
                ReporteErrores.func(error)
                return 
                
        #PAND
        elif(self.tipo == TIPO_OPERACION.PAND):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            valor1 = int(valor1)
            valor2 = int(valor2)

            return valor1 & valor2

        #BOR
        elif(self.tipo == TIPO_OPERACION.BOR):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            valor1 = int(valor1)
            valor2 = int(valor2)

            return valor1 | valor2

        #XORR
        elif(self.tipo == TIPO_OPERACION.XORR):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            valor1 = int(valor1)
            valor2 = int(valor2)

            return valor1 ^ valor2

        #SHIFI
        elif(self.tipo == TIPO_OPERACION.SHIFTI):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            valor1 = int(valor1)
            valor2 = int(valor2)

            return valor1 << valor2

        #SHIFD
        elif(self.tipo == TIPO_OPERACION.SHIFTD):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            valor2 = self.operadorDer.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            if(isinstance(valor2,str)): valor2 = self.obtenerValorNumerico(valor2)

            valor1 = int(valor1)
            valor2 = int(valor2)

            return valor1 >> valor2

        #NOTR
        elif(self.tipo == TIPO_OPERACION.NOTR):
            valor1 = self.operadorIzq.getValorImplicito(ent,arbol)
            if(isinstance(valor1,str)): valor1 = self.obtenerValorNumerico(valor1)
            valor1 = int(valor1)
            return ~valor1
        

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

    