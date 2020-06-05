import ascendente as g
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.GoTo as GoTo
import ast.Declaracion as Declaracion
import Primitivas.Exit as Exit
import Condicionales.If as If
import ast.AST as AST
import Reporteria.Error as Error
import Reporteria.ReporteErrores as ReporteErrores
import Reporteria.ReporteTablaSimbolos as ReporteTablaSimbolos
import sys
sys.setrecursionlimit(20000)

f = open("./etiquetas.txt", "r")
input = f.read()

listadoErrores = []
g.textoEntrada = input
instrucciones = g.parse(input)
ts_global = TS.Entorno(None)
ast = AST.AST(instrucciones) 

declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"")
declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"")
declaracion1.ejecutar(ts_global,ast)
declaracion2.ejecutar(ts_global,ast)


#PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
if(instrucciones != None):
    for ins in instrucciones:
        try:
            if(ast.existeEtiqueta(ins)):
                error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                ReporteErrores.func(error)
            else:
                ast.agregarEtiqueta(ins)
        except:
                pass

main = ast.obtenerEtiqueta("main")

if(main != None):
    salir = False
    for ins in main.instrucciones:
        try:
            if(type(ins) is Exit.Exit): 
                break
            resultado = ins.ejecutar(ts_global,ast)
            if(type(resultado) is Exit.Exit): 
                salir = True
                break
            elif((type(ins) is If.If) or (type(ins) is GoTo.GoTo)) and resultado == True:
                salir = True
                break
        except:
            pass

    if(not salir):   
        siguiente = ast.obtenerSiguienteEtiqueta("main")
        if(siguiente!=None):
            siguiente.ejecutar(ts_global,ast)
else:
    error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",ins.linea,ins.columna)
    ReporteErrores.func(error)

#reporteErrores = ReporteErrores.ReporteErrores()
#reporteErrores.generarReporte()

#reporteTablas = ReporteTablaSimbolos.ReporteTablaSimbolos()
#reporteTablas.generarReporte(ts_global,ast)