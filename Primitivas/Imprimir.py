from ast.Instruccion import Instruccion

class Imprimir(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

    def ejecutar(self,ent,arbol):
        print('> ', self.cad.getValorImplicito(ent,arbol))