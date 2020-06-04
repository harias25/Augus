from ast.Instruccion import Instruccion

class Imprimir(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

    def ejecutar(self,ent,arbol):
        valor = self.cad.getValorImplicito(ent,arbol)
        if(isinstance(valor,dict)):
            print("Error, no es posible imprimir un Array!!")
        elif(valor == None):
            return None
        else:
            print('> ', valor)