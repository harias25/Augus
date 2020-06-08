from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
import ast.Entorno as TS
import Primitivas.Exit as Exit
import Condicionales.If as If
import ast.GoTo as GoTo
import ValorImplicito.Asignacion as Asignacion
import ValorImplicito.Conversion as Conversion

class Etiqueta(Instruccion) :
    def __init__(self,  id, instrucciones,linea,columna) :
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        
        salir = False

        for ins in self.instrucciones:
            #try:
                if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                    ins.setAmbito(self.id)
                if(ins.ejecutar(ent,arbol,ventana,isDebug) == True):
                    return True
            #except:
            #    pass

        if(not salir):
            siguiente = arbol.obtenerSiguienteEtiqueta(self.id)
            if(siguiente!=None):
                if(siguiente.ejecutar(ent,arbol,ventana,isDebug) == True):
                    return True
                
        return False

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