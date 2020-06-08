from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Primitivo import Primitivo
from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

class AccesoLista(Expresion,Instruccion):
    def __init__(self,id,llaves,valor,linea,columna,DefArray):
        self.id             = id    
        self.llaves         = llaves  
        self.linea          = linea
        self.columna        = columna
        self.asignacion     = valor
        self.defArray       = DefArray
    
    def ejecutar(self,ent,arbol,ventana,isDebug):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, No existe la variable con identificador "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return False

        valorIdentificador = simbolo.valor

        valorAgregar = None
        if not self.defArray:
            valorAgregar = self.asignacion.getValorImplicito(ent,arbol)

        if(valorAgregar==None and not self.defArray): return False

        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(valor == None): return False
            if(isinstance(valor,float)): valor = int(valor)

            if(not isinstance(valorIdentificador,dict) and self.defArray):
                error = Error("SEMANTICO","Error semantico, Solo pueden inicializarse array dento de arrays",self.linea,self.columna)
                ReporteErrores.func(error)
                return False

            if(isinstance(valorIdentificador,str)):  #cadenas
                if len(self.llaves) > 1:
                    error = Error("SEMANTICO","Error semantico, No puede usarse acceso [..][..]... para asignación de Cadenas",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return False

                if(isinstance(valorAgregar,float)): valorAgregar = int(valorAgregar)
                if(isinstance(valorAgregar,dict)):
                    error = Error("SEMANTICO","Error semantico, Valor no valido para asignar caracteres de una cadena",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return False
                if(isinstance(valor,int)):
                    if(valor<=(len(valorIdentificador)-1)):
                        valorAgregar = str(valorAgregar)[0] 
                        valorIdentificador = valorIdentificador[0:valor] + valorAgregar + valorIdentificador[valor+1:len(valorIdentificador)]
                    else:
                        while (len(valorIdentificador)-1)!= valor-1:
                            valorIdentificador = valorIdentificador + ' '

                        valorAgregar = str(valorAgregar)[0] 
                        valorIdentificador = valorIdentificador + valorAgregar

                    asignar = Asignacion(self.id,Primitivo(valorIdentificador,0,0),self.linea,self.columna,False)
                    asignar.ejecutar(ent,arbol,ventana,isDebug)
                else:
                    error = Error("SEMANTICO","Error semantico, Llave no valida para asingar caracteres de una cadena",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return False
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                valorFinal = self.asignarValorEnArray(ent,valorIdentificador,valorAgregar,1)
                if(valorFinal == None): return False
                asignar = Asignacion(self.id,Primitivo(valorIdentificador,0,0),self.linea,self.columna,False)
                asignar.ejecutar(ent,arbol,ventana,isDebug)
            else:
                error = Error("SEMANTICO","Error semantico, el valor del acceso no es de tipo CADENA O ARRAY",self.linea,self.columna)
                ReporteErrores.func(error)
                return False

    def asignarValorEnArray(self,ent,diccionario,valorAgregar,pos):
        temporal = diccionario

        if((isinstance(temporal,int) or isinstance(temporal,float)) and pos > 1):
            error = Error("SEMANTICO","Error semantico, Ya se encuentra ocupado el indice.",self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(len(self.llaves)<pos): return None

        llave=self.llaves[pos-1]
        valor = llave.getValorImplicito(ent,None)

        if(valor == None): return None
        if(isinstance(valor,float)): valor = int(valor)

        if(len(self.llaves)==pos):
            if(isinstance(temporal,dict)):
                if(self.defArray):
                    temporal[valor] = {}
                else:
                    temporal[valor] = valorAgregar
            elif isinstance(temporal,str):
                if(self.defArray):
                    error = Error("SEMANTICO","Error semantico, solo pueden inicializarse array dento de arrays",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return None
                else:
                    if(isinstance(valor,int)):
                        if(valor<=(len(temporal)-1)):
                            valorAgregar = str(valorAgregar)[0] 
                            temporal = temporal[0:valor] + valorAgregar + temporal[valor+1:len(temporal)]
                        else:
                            while (len(temporal)-1)!= valor-1:
                                temporal = temporal + ' '

                            valorAgregar = str(valorAgregar)[0] 
                            temporal = temporal + valorAgregar

                        return temporal
                    else:
                        error = Error("SEMANTICO","Error semantico, Llave no valida para asingar caracteres de una cadena",self.linea,self.columna)
                        ReporteErrores.func(error)
                        return None
            return temporal
        else:
            if(isinstance(temporal,dict)):
                if valor not in temporal.keys():
                    temporal[valor] = {}
            else:
                error = Error("SEMANTICO","Error semantico, Asignación incorrecta a un valor que no es un Array",self.linea,self.columna)
                ReporteErrores.func(error)
                return None

        resultado = self.asignarValorEnArray(ent,temporal[valor],valorAgregar,pos+1)
        if(resultado == None and isinstance(temporal[valor],dict)): return diccionario
        if(resultado == None and not isinstance(temporal[valor],dict)): return None
        diccionario[valor] = resultado
        return diccionario

    def getValorImplicito(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, No existe la variable con identificador "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        valorIdentificador = simbolo.valor
        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(isinstance(valor,float)): valor = int(valor)

            if(isinstance(valorIdentificador,str)):  #cadenas
                if(isinstance(valor,int)):
                    if(valor >= len(valorIdentificador)):
                        error = Error("SEMANTICO","Error semantico, El indice excede el tamaño de la cadena",self.linea,self.columna)
                        ReporteErrores.func(error)
                        return None
                    valorIdentificador = valorIdentificador[valor]
                else:
                    error = Error("SEMANTICO","Error semantico, Llave no valida para obtener caracteres de una cadena",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return None
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                if(isinstance(valor,dict)): 
                    error = Error("SEMANTICO","Error semantico, Llave no valida para obtener valor del Array",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return None
                if valor not in valorIdentificador.keys():
                    error = Error("SEMANTICO","Error semantico, Llave "+str(valor)+" no existente en el Array",self.linea,self.columna)
                    ReporteErrores.func(error)
                    return None
                else:
                    valorIdentificador = valorIdentificador[valor]
            else:
                error = Error("SEMANTICO","Error semantico, el valor del acceso no es de tipo CADENA O ARRAY",self.linea,self.columna)
                ReporteErrores.func(error)
                return None

        return valorIdentificador

    
    
