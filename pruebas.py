import ascendente as g
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.Declaracion as Declaracion
import Primitivas.Exit as Exit
import ast.AST as AST

f = open("./etiquetas.txt", "r")
input = f.read()

g.textoEntrada = input
instrucciones = g.parse(input)
ts_global = TS.Entorno(None)
ast = AST.AST(instrucciones) 

declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"")
declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"")
declaracion1.ejecutar(ts_global,ast)
declaracion2.ejecutar(ts_global,ast)


#PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
for ins in instrucciones:
    if(ast.existeEtiqueta(ins)):
        print("Ya existe una etiqueta "+ins.id)
    else:
        ast.agregarEtiqueta(ins)

main = ast.obtenerEtiqueta("main")

if(main != None):
    for ins in main.instrucciones:
        if(type(ins) is Exit.Exit): 
            break
        resultado = ins.ejecutar(ts_global,ast)
        if(type(resultado) is Exit.Exit): 
            break
        
    siguiente = ast.obtenerSiguienteEtiqueta("main")
    if(siguiente!=None):
        siguiente.ejecutar(ts_global,ast)
        
else:
    print("no puede iniciarse el programa ya que no existe la etiqueta main:")



