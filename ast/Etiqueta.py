from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
import ast.Entorno as TS
import Primitivas.Exit as Exit
import Condicionales.If as If
import ast.GoTo as GoTo

class Etiqueta(Instruccion) :
    def __init__(self,  id, instrucciones,linea,columna) :
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol):
        
        salir = False

        for ins in self.instrucciones:
            try:
                if(type(ins) is Exit.Exit): 
                    return ins
                resultado = ins.ejecutar(ent,arbol)
                if(type(resultado) is Exit.Exit): 
                    return resultado
                elif((type(ins) is If.If) or (type(ins) is GoTo.GoTo)) and resultado == True:
                    salir = True
                    break
            except:
                pass

        if(not salir):
            siguiente = arbol.obtenerSiguienteEtiqueta(self.id)
            if(siguiente!=None):
                siguiente.ejecutar(ent,arbol)
 
        return None

    def getTipo(self):
        isProc = False
        isFunc = False

        for ins in self.instrucciones:
            try:
                if(type(ins) is Asignacion):
                    if(ins.id.startswith('$a')):
                        isProc = True
                    
                    if(ins.id.startswith('$v')):
                        isFunc = True
                        break

            except:
                pass
            
        if(isFunc and isProc): return "FUNCION"
        if(isProc): return "PROCEDIMIENTO"
            
        return "ETIQUETA"