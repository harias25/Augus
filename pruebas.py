import gramatica_old as g
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.AST as AST

f = open("./proyecto.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.Entorno(None)
ast = AST.AST(instrucciones) 

for ins in instrucciones:
    ins.ejecutar(ts_global,ast)

