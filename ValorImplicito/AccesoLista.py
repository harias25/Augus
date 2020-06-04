from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Primitivo import Primitivo
from ast.Instruccion import Instruccion
from ast.Expresion import Expresion

class AccesoLista(Expresion,Instruccion):
    def __init__(self,id,llaves,valor,linea,columna):
        self.id             = id    
        self.llaves         = llaves  
        self.linea          = linea
        self.columna        = columna
        self.asignacion     = valor
    
    def ejecutar(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            print("No existe la variable con identificador "+self.id)
            return None

        valorIdentificador = simbolo.valor
        valorAgregar = self.asignacion.getValorImplicito(ent,arbol)

        if(valorAgregar==None): return None

        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(isinstance(valor,float)): valor = int(valor)

            if(isinstance(valorIdentificador,str)):  #cadenas

                if len(self.llaves) > 1:
                    print("No puede usarse acceso [..][..]... para asignación de Cadenas")
                    return None

                if(isinstance(valorAgregar,float)): valorAgregar = int(valorAgregar)
                if(isinstance(valorAgregar,dict)):
                    print("Valor no valido para asignar caracteres de una cadena")
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
                    return None
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                return 0 
            else:
                print("Error semantico, el valor del acceso no es de tipo CADENA O ARRAY")
                return None


    def getValorImplicito(self,ent,arbol):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            print("No existe la variable con identificador "+self.id)
            return None

        valorIdentificador = simbolo.valor
        for llave in self.llaves:
            valor = llave.getValorImplicito(ent,arbol)
            if(isinstance(valor,float)): valor = int(valor)

            if(isinstance(valorIdentificador,str)):  #cadenas
                if(isinstance(valor,int)):
                    if(valor >= len(valorIdentificador)):
                        print("El indice excede el tamaño de la cadena")
                        return None
                    valorIdentificador = valorIdentificador[valor]
                else:
                    print("Llave no valida para obtener caracteres de una cadena")
                    return None
            elif(isinstance(valorIdentificador,dict)):  #diccionarios
                return 0 
            else:
                print("Error semantico, el valor del acceso no es de tipo CADENA O ARRAY")
                return None

        return valorIdentificador

    
    
