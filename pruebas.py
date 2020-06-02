import ascendente as g
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.Declaracion as Declaracion
import Primitivas.Exit as Exit
import ast.AST as AST

f = open("./proyecto.txt", "r")
input = f.read()

g.textoEntrada = input
instrucciones = g.parse(input)
ts_global = TS.Entorno(None)
ast = AST.AST(instrucciones) 

declaracion1 = Declaracion.Declaracion('$ra',0,0,0,False)
declaracion2 = Declaracion.Declaracion('$sp',0,0,0,False)
declaracion1.ejecutar(ts_global,ast)
declaracion2.ejecutar(ts_global,ast)

for ins in instrucciones:
    if(type(ins) is Exit.Exit): 
        break
    ins.ejecutar(ts_global,ast)

