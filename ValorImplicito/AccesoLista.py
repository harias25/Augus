from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Primitivo import Primitivo
from ast.Instruccion import Instruccion
from ast.Expresion import Expresion

class AccesoLista(Expresion,Instruccion):
    def __init__(self,id,llaves,valor,linea,columna,DefArray):
        self.id             = id    
        self.llaves         = llaves  
        self.linea          = str(linea)
        self.columna        = str(columna)
        self.asignacion     = valor
        self.defArray       = DefArray
    
    def ejecutar(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            print("No existe la variable con identificador "+self.id)
            print("Linea: "+self.linea)
            print("Columna: "+self.columna)
            return None

        valorIdentificador = simbolo.valor

        valorAgregar = None
        if not self.defArray:
            valorAgregar = self.asignacion.getValorImplicito(ent,arbol)

        if(valorAgregar==None and not self.defArray): return None

        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(valor == None): return None
            if(isinstance(valor,float)): valor = int(valor)

            if(not isinstance(valorIdentificador,dict) and self.defArray):
                print("Solo pueden inicializarse array dento de arrays")
                print("Linea: "+self.linea)
                print("Columna: "+self.columna)
                return None

            if(isinstance(valorIdentificador,str)):  #cadenas
                if len(self.llaves) > 1:
                    print("No puede usarse acceso [..][..]... para asignación de Cadenas")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None

                if(isinstance(valorAgregar,float)): valorAgregar = int(valorAgregar)
                if(isinstance(valorAgregar,dict)):
                    print("Valor no valido para asignar caracteres de una cadena")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None
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
                    asignar.ejecutar(ent,arbol)
                else:
                    print("Llave no valida para asingar caracteres de una cadena")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                valorFinal = self.asignarValorEnArray(ent,valorIdentificador,valorAgregar,1)
                if(valorFinal == None): return None
                asignar = Asignacion(self.id,Primitivo(valorIdentificador,0,0),self.linea,self.columna,False)
                asignar.ejecutar(ent,arbol)
            else:
                print("Error semantico, el valor del acceso no es de tipo CADENA O ARRAY")
                print("Linea: "+self.linea)
                print("Columna: "+self.columna)
                return None

    def asignarValorEnArray(self,ent,diccionario,valorAgregar,pos):
        temporal = diccionario

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
                    print("Solo pueden inicializarse array dento de arrays")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
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
                        print("Llave no valida para asingar caracteres de una cadena")
                        print("Linea: "+self.linea)
                        print("Columna: "+self.columna)
                        return None
        else:
            if(isinstance(temporal,dict)):
                if valor not in temporal.keys():
                    temporal[valor] = {}
            else:
                print("Asignación incorrecta a un valor que no es un Array")
                print("Linea: "+self.linea)
                print("Columna: "+self.columna)
                return None

        resultado = self.asignarValorEnArray(ent,temporal[valor],valorAgregar,pos+1)
        if(resultado == None): return diccionario

        diccionario[valor] = resultado
        return diccionario

    def getValorImplicito(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            print("No existe la variable con identificador "+self.id)
            print("Linea: "+self.linea)
            print("Columna: "+self.columna)
            return None

        valorIdentificador = simbolo.valor
        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(isinstance(valor,float)): valor = int(valor)

            if(isinstance(valorIdentificador,str)):  #cadenas
                if(isinstance(valor,int)):
                    if(valor >= len(valorIdentificador)):
                        print("El indice excede el tamaño de la cadena")
                        print("Linea: "+self.linea)
                        print("Columna: "+self.columna)
                        return None
                    valorIdentificador = valorIdentificador[valor]
                else:
                    print("Llave no valida para obtener caracteres de una cadena")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                if(isinstance(valor,dict)): 
                    print("Llave no valida para obtener valor del Array")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None
                if valor not in valorIdentificador.keys():
                    print("Llave "+str(valor)+" no existente en el Array")
                    print("Linea: "+self.linea)
                    print("Columna: "+self.columna)
                    return None
                else:
                    valorIdentificador = valorIdentificador[valor]
            else:
                print("Error semantico, el valor del acceso no es de tipo CADENA O ARRAY")
                print("Linea: "+self.linea)
                print("Columna: "+self.columna)
                return None

        return valorIdentificador

    
    
