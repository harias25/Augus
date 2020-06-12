# Definición de la gramática
from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ast.Etiqueta import Etiqueta
from ast.GoTo import GoTo
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.Operacion import Operacion
from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Conversion import Conversion
from ValorImplicito.Operacion import TIPO_OPERACION
from ValorImplicito.Primitivo import Primitivo
from ValorImplicito.AccesoLista import AccesoLista
from ValorImplicito.Read import Read
from  Primitivas.Imprimir import Imprimir
from  Primitivas.Unset import Unset
from  Primitivas.Exit import Exit
from  Condicionales.If import If
import ply.yacc as yacc
import Reporteria.Error as Error
import Reporteria.ValorAscendente as G
import Reporteria.ReporteErrores as ReporteErrores

reservadas = {
    'int'	: 'INT',
    'float' : 'FLOAT',
    'char'	: 'CHAR',
    'goto'	: 'GOTO',
    'exit'  : 'EXIT',
    'abs'   : 'ABS',
    'print' : 'IMPRIMIR',
    'unset' : 'UNSET',
    'if'	: 'IF',
	'xor'	: 'XOR',
    'read'  : 'READ',
    'array' : 'ARRAY'
}

tokens  = [
    'PTCOMA',
	'DOSP',
    'PARIZQ',
    'PARDER',
	'CORIZQ',
    'CORDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'RESTO',
    'MENQUE',
    'MAYQUE',
    'MEIQUE',
    'MAIQUE',
    'IGUALQUE',
    'NIGUALQUE',
	'AND',
    'OR',
	'NOTR',
    'NOT',
	'XORR',
	'SHIFTI',
	'SHIFTD',
    'TEMP',
	'PARAM',
	'RET',
	'PILA',
    'ID',
	'DECIMAL',
    'ENTERO',
    'CADENA',
    'CADENA2',
    'PAND',
    'RA',
    'PUNTERO',
    'BOR'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSP		= r':'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_RESTO     = r'%'

t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_MEIQUE    = r'<='
t_MAIQUE    = r'>='
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='

t_PAND       = r'&'
t_BOR       = r'\|'

t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOTR		= r'~'
t_NOT       = r'!'
t_XORR       = r'\^'

t_SHIFTI    = r'<<'
t_SHIFTD    = r'>>'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_TEMP(t):
     r'[$][tT][0-9]+'
     t.type = reservadas.get(t.value.lower(),'TEMP')    # Check for reserved words
     return t

def t_PARAM(t):
     r'[$][aA][0-9]+'
     t.type = reservadas.get(t.value.lower(),'PARAM')    # Check for reserved words
     return t

def t_RET(t):
     r'[$][vV][0-9]+'
     t.type = reservadas.get(t.value.lower(),'RET')    # Check for reserved words
     return t

def t_PILA(t):
     r'[$][sS][0-9]+'
     t.type = reservadas.get(t.value.lower(),'PILA')    # Check for reserved words
     return t

def t_RA(t):
    r'[$][rR][aA]'
    t.type = reservadas.get(t.value.lower(),'RA')    # Check for reserved words
    return t

def t_PUNTERO(t):
    r'[$][sS][pP]'
    t.type = reservadas.get(t.value.lower(),'PUNTERO')    # Check for reserved words
    return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADENA2(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
     r'\n+'
     t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    error = Error.Error("LEXICO","Error lexico, Caracter "+t.value[0]+" no es valido.",t.lexer.lineno,find_column(t))
    ReporteErrores.func(error)
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

textoEntrada = ""
# Funcion para obtener la columna
def find_column(token):
    line_start = textoEntrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    #('left','CONCAT'),
    ('left','OR'),
    ('left','AND'),
    ('nonassoc','MENQUE','MAYQUE','MEIQUE','MAIQUE','IGUALQUE','NIGUALQUE'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','RESTO'),
    ('right','UMENOS','NOT','NOTR'),
    )

#precedence nonassoc menor,mayor, menor_igual,mayor_igual;
def func(tipo,valor):
 
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(func,"listado"):
        func.listado = []

    if(tipo==0):
        func.listado = []

    if(valor!=None):
        func.listado.append(valor)

    if(tipo==1):
        return func.listado


def p_init(t) :
    'init            : etiquetas'
    t[0] = t[1]

def p_init_empty(t):
    'init            : empty'
    t[0] = t[1]

#********************************************** ETIQUETAS  **************************************
def p_etiquetas_lista(t) :
    'etiquetas    : etiquetas etiqueta'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('etiquetas -> etiquetas etiqueta','etiquetas.lista = etiquetas1.lista; </hr> etiquetas.lista.add(etiqueta)',None)
    func(2,gramatical)

def p_etiquetas(t) :
    'etiquetas    : etiqueta '
    t[0] = [t[1]]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('etiquetas -> etiqueta','etiquetas.lista = [etiqueta]',lista)
    func(0,gramatical)

def p_empty(t) :
    'empty :'
    t[0] = []

def p_etiqueta(t) :
    'etiqueta    : ID DOSP instrucciones '
    lista = func(1,None).copy()
    t[0] = Etiqueta(t[1],t[3],t.slice[1].lineno,find_column(t.slice[1]))
    gramatical = G.ValorAscendente('etiqueta -> ID DOSP instrucciones','etiqueta.instrucciones.lista = []; </hr> etiqueta.instrucciones.lista = instrucciones.lista;',lista)
    func(0,gramatical)

def p_etiqueta_e(t) :
    'etiqueta    : ID DOSP empty '
    t[0] = Etiqueta(t[1],t[3],t.slice[1].lineno,find_column(t.slice[1]))    
    gramatical = G.ValorAscendente('etiqueta -> ID DOSP','etiqueta.instrucciones.lista = [];',[])
    func(2,gramatical)#func(2,gramatical)
#********************************************** INSTRUCCIONES  ***********************************

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instrucciones -> instrucciones instruccion','instrucciones.lista = instrucciones1.lista; </hr> instrucciones.lista.add(instruccion);',[])
    func(2,gramatical)#func(0,gramatical)

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instrucciones -> instruccion','instrucciones.lista = [instruccion]',[])
    func(2,gramatical)#func(0,gramatical)

def p_instruccion(t) :
    '''instruccion      : imprimir_instr 
                        | asignacion 
                        | unset 
                        | exit 
                        | puntero        
                        | go_to 
                        | if_instruccion
                        | conversion
                        | acceso_lista_asigna
                        | read
                        | error '''
    t[0] = t[1]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instruccion -> '+str(t.slice[1]),'instruccion.instr = '+str(t.slice[1])+'.instr;',lista)
    func(0,gramatical)

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ tipo_var PARDER PTCOMA'
    op = Operacion()
    op.Indentficador(t[3],t.slice[1].lineno,find_column(t.slice[2]))
    op.linea = t.slice[1].lineno
    op.columna = find_column(t.slice[1])
    t[0] =Imprimir(op,t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ tipo_var  PARDER PTCOMA','imprimir_instr.instr = Print(tipo_var.val);',lista)
    func(0,gramatical)

def p_instruccion_imprimir_acceso(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ acceso_lista PARDER PTCOMA'
    t[0] =Imprimir(t[3],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ acceso_lista  PARDER PTCOMA','imprimir_instr.instr = Print(acceso_lista.val);',lista)
    func(0,gramatical)

def p_instruccion_imprimir_cadena(t) :
    '''imprimir_instr     : IMPRIMIR PARIZQ CADENA  PARDER PTCOMA
                          | IMPRIMIR PARIZQ CADENA2 PARDER PTCOMA'''
    op = Operacion()
    op.Primitivo(Primitivo(t[3],t.slice[1].lineno,0))
    op.linea = t.slice[1].lineno
    op.columna = find_column(t.slice[1])
    t[0] = Imprimir(op,t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ CADENA  PARDER PTCOMA','imprimir_instr.instr = Print(CADENA);',lista)
    func(0,gramatical)

def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_relacional
                 | expresion_unaria
                 | expresion_logica 
                 | expresion_bit_bit
                 | absoluto'''
    t[0] = t[1]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion -> '+str(t.slice[1]),'expresion.val = '+str(t.slice[1])+'.val;',lista)
    func(0,gramatical)

#********************************************** INSTRUCCIONES PRIMITIVAS ***********************************
def p_go_to(t):
    'go_to : GOTO ID PTCOMA'
    t[0] = GoTo(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('go_to ->GOTO ID PTCOMA','go_to.instr = GoTO(ID);',lista)
    func(0,gramatical)
    
def p_if(t):
    'if_instruccion : IF PARIZQ expresion PARDER go_to '
    t[0] = If(t[3],t[5],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('if_instruccion -> IF PARIZQ expresion PARDER go_to','if_instruccion.instr = If(expresion.val,go_to.instr);',lista)
    func(0,gramatical)
def p_exit(t):
    'exit : EXIT PTCOMA'
    t[0] = Exit(t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('exit -> EXIT PTCOMA','exit.instr = Exit();',lista)
    func(0,gramatical)
def p_unset(t):
    '''unset : UNSET PARIZQ TEMP PARDER PTCOMA
             | UNSET PARIZQ PARAM PARDER PTCOMA
             | UNSET PARIZQ RET PARDER PTCOMA
             | UNSET PARIZQ PILA PARDER PTCOMA'''
    t[0] = Unset(t[3],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('unset -> UNSET PARIZQ tipo_var PARDER PTCOMA','unset.instr = Unset(tipo_var.val);',lista)
    func(0,gramatical)
#********************************************** ASIGNACIONES *********************************************
def p_read(t):
    'read : tipo_var IGUAL READ PARIZQ PARDER PTCOMA'
    t[0] = Read(t[1],t.slice[2].lineno,1)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('read -> tipo_var IGUAL read() PTCOMA','read.instr = Read(tipo_var.val);',lista)
    func(0,gramatical)

def p_asignacion(t):
    'asignacion : tipo_var IGUAL expresion PTCOMA '
    t[0] = Asignacion(t[1],t[3],t.slice[2].lineno,1,False)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('asignacion -> tipo_var IGUAL expresion PTCOMA','asignacion.instr = Asignar(tipo_var.val,expresion.val);',lista)
    func(0,gramatical)

def p_asingacion_array(t):
    'asignacion : tipo_var IGUAL ARRAY PARIZQ PARDER PTCOMA '
    t[0] = Asignacion(t[1],{},t.slice[2].lineno,1,False)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('asignacion -> tipo_var IGUAL ARRAY PARIZQ PARDER PTCOMA','asignacion.instr = Asignar(tipo_var.val,new Array());',lista)
    func(0,gramatical)

def p_puntero(t):
    'puntero : tipo_var IGUAL PAND  tipo_var PTCOMA '
    op = Operacion()
    op.Indentficador(t[4],t.slice[2].lineno,find_column(t.slice[3])+1)
    t[0] = Asignacion(t[1],op,t.slice[2].lineno,1,True)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('puntero -> tipo_var IGUAL PAND  tipo_var PTCOMA','puntero.instr = Puntero(tipo_var1.val,tipo_var2.val);',lista)
    func(0,gramatical)
    
def p_conversiones(t):
    'conversion : tipo_var IGUAL PARIZQ tipo_dato PARDER primitiva PTCOMA '
    t[0] = Conversion(t[1],t[6],t[4],t.slice[2].lineno,1)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('conversion -> tipo_var IGUAL  PARIZQ tipo_dato PARDER primitiva PTCOMA','conversion.instr = Conversion(tipo_var.val,tipo_dato.val,primitiva.val);',lista)
    func(0,gramatical)
def p_tipo_dato(t):
    '''tipo_dato : INT 
                | FLOAT 
                | CHAR '''
    t[0] = t[1]
    gramatical = G.ValorAscendente('tipo_dato -> '+str(t[1]),'tipo_dato.val = '+str(t[1])+';',None)
    func(2,gramatical)

def p_tipo_var(t):
    '''tipo_var : TEMP 
                | PARAM 
                | RET 
                | PILA 
                | RA
                | PUNTERO '''
    t[0] = t[1]
    gramatical = G.ValorAscendente('tipo_var -> '+str(t.slice[1].type),'tipo_var.val = '+str(t.slice[1].type)+';',None)
    func(2,gramatical)
#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS primitiva %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    t[0] = op
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_unaria ->  MENOS primitiva %prec UMENOS','expresion_unaria.val = -primitiva.val;',lista)
    func(0,gramatical)
#********************************************** OPERACIONES LOGICAS ***********************************
def p_expresion_logica(t):
    '''expresion_logica   : primitiva AND primitiva 
                          | primitiva OR primitiva
                          | primitiva XOR primitiva '''
                          
    op = Operacion()
    if(t.slice[2].type == 'AND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.AND,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  primitiva AND primitiva','expresion_logica.val = primitiva1.val && primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'OR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.OR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  primitiva OR primitiva','expresion_logica.val = primitiva1.val || primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'XOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XOR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  primitiva XOR primitiva','expresion_logica.val = primitiva1.val xor primitiva2.val;',lista)
        func(0,gramatical)
    t[0] = op

def p_expresion_negacion(t):
    'expresion_logica   :   NOT primitiva %prec NOT' 
    op = Operacion()
    op.OperacionNot(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    t[0] = op    
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_logica ->  NOT primitiva %prec NOT','expresion_logica.val = !primitiva.val;',lista)
    func(0,gramatical)
#********************************************** OPERACIONES BIT A BIT ***********************************
def p_expresion_bit_bit(t):
    '''expresion_bit_bit  : primitiva PAND primitiva 
                          | primitiva BOR primitiva
                          | primitiva XORR primitiva 
                          | primitiva SHIFTI primitiva
                          | primitiva SHIFTD primitiva'''
                          
    op = Operacion()
    if(t.slice[2].type == 'PAND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.PAND,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  primitiva PAND primitiva','expresion_bit_bit.val = primitiva1.val & primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'BOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.BOR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  primitiva BOR primitiva','expresion_bit_bit.val = primitiva1.val | primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'XORR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XORR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  primitiva XORR primitiva','expresion_bit_bit.val = primitiva1.val ^ primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'SHIFTI'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTI,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  primitiva SHIFTI primitiva','expresion_bit_bit.val = primitiva1.val << primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'SHIFTD'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTD,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  primitiva SHIFTD primitiva','expresion_bit_bit.val = primitiva1.val >> primitiva2.val;',lista)
        func(0,gramatical)
    t[0] = op

def p_expresion_negacion_bit(t):
    'expresion_bit_bit   :   NOTR primitiva %prec NOTR' 
    op = Operacion()
    op.OperacionNotBit(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_bit_bit ->  NOTR primitiva %prec NOTR','expresion_bit_bit.val = ~primitiva.val;',lista)
    func(0,gramatical)
    t[0] = op   
#********************************************** OPERACIONES RELACIONALES ***********************************
def p_expresion_relacional(t):
    '''expresion_relacional :   primitiva MENQUE primitiva 
                            |   primitiva MAYQUE primitiva 
                            |   primitiva MEIQUE primitiva
                            |   primitiva MAIQUE primitiva
                            |   primitiva IGUALQUE primitiva 
                            |   primitiva NIGUALQUE primitiva '''
    op = Operacion()
    if(t.slice[2].type == 'MENQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva MENOR primitiva','expresion_relacional.val = primitiva1.val < primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MAYQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva MAYOR primitiva','expresion_relacional.val = primitiva1.val > primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MEIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_IGUA_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva MENORIGUAL primitiva','expresion_relacional.val = primitiva1.val <= primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MAIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_IGUA_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva MAYORIGUAL primitiva','expresion_relacional.val = primitiva1.val >= primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'IGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.IGUAL_IGUAL,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva IGUAL IGUAL primitiva','expresion_relacional.val = primitiva1.val == primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'NIGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIFERENTE_QUE,t.slice[2].lineno,1)    
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  primitiva DIFERENTE primitiva','expresion_relacional.val = primitiva1.val != primitiva2.val;',lista)
        func(0,gramatical)
    t[0] = op
#********************************************** OPERACIONES ARITMETICAS ***********************************
def p_expresion_numerica(t):
    '''expresion_numerica   :   primitiva MAS primitiva 
                            |   primitiva MENOS primitiva 
                            |   primitiva POR primitiva
                            |   primitiva DIVIDIDO primitiva
                            |   primitiva RESTO primitiva'''

    op = Operacion()
    if(t.slice[2].type == 'MAS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SUMA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  primitiva MAS primitiva','expresion_numerica.val = primitiva1.val + primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.RESTA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  primitiva MENOS primitiva','expresion_numerica.val = primitiva1.val - primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'POR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  primitiva MULT primitiva','expresion_numerica.val = primitiva1.val * primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIVISION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  primitiva DIV primitiva','expresion_numerica.val = primitiva1.val / primitiva2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'RESTO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MODULO,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  primitiva RESTO primitiva','expresion_numerica.val = primitiva1.val % primitiva2.val;',lista)
        func(0,gramatical)
    t[0] = op

#********************************************** EXPRESIONES PRIMITIVAS ***********************************

def p_absoluto(t):
    'absoluto : ABS PARIZQ primitiva PARDER '
    op = Operacion()
    op.ValorAbsoluto(t[3],t.slice[1].lineno,find_column(t.slice[1]))
    t[0] = op
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('absoluto ->  ABS PARIZQ primitiva PARDER','absoluto.val = Math.ABS(primitiva.val);',lista)
    func(0,gramatical)

def p_expresion_primitiva(t):
    '''primitiva : ENTERO
                 | DECIMAL
                 | CADENA
                 | CADENA2
                 | TEMP 
                 | PARAM
                 | RET
                 | PILA 
                 | RA
                 | PUNTERO 
                 | acceso_lista'''
    op = Operacion()
    if(t.slice[1].type == 'CADENA' or t.slice[1].type == 'CADENA2'):
        op.Primitivo(Primitivo(str(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> CADENA','primitiva.val = str(CADENA);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'DECIMAL'):
        op.Primitivo(Primitivo(float(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> FLOAT','primitiva.val = float(FLOAT);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'ENTERO'):
        op.Primitivo(Primitivo(int(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> ENTERO','primitiva.val = int(ENTERO);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'TEMP') or (t.slice[1].type == 'PARAM') or (t.slice[1].type == 'RET') or (t.slice[1].type == 'PILA') or (t.slice[1].type == 'RA') or (t.slice[1].type == 'PUNTERO'):
        op.Indentficador(t[1],t.slice[1].lineno,find_column(t.slice[1]))
        op.linea = t.slice[1].lineno
        op.columna = find_column(t.slice[1])
        gramatical = G.ValorAscendente('primitiva -> tipo_var','primitiva.val = tipo_var.val;',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'acceso_lista'):
        op.linea = t.lexer.lineno
        op.columna = 1
        op.AccesoLista(t[1],t.lexer.lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('primitiva ->  acceso_lista','primitiva.val = acceso_lista.val;',lista)
        func(0,gramatical)
    t[0] = op

#********************************************** LISTAS *******************************************
def  p_acceso_lista(t):
    'acceso_lista : tipo_var accesos'
    t[0] = AccesoLista(t[1],t[2],None,t.lexer.lineno,1,False)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('acceso_lista ->  tipo_var accesos','acceso_lista.val = AccesoLista(tipovar.val,accesos.lista,Null);',lista)
    func(0,gramatical)

def  p_acceso_lista_asigna(t):
    'acceso_lista_asigna : tipo_var accesos IGUAL expresion PTCOMA'
    t[0] = AccesoLista(t[1],t[2],t[4],t.slice[3].lineno,1,False)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('acceso_lista_asigna ->  tipo_var accesos IGUAL ARRAY PARIZQ PARDER PTCOMA','acceso_lista_asigna.inst = AccesoLista(tipovar.val,accesos.lista,expresion.val);',lista)
    func(0,gramatical)

def  p_acceso_lista_asigna_array(t):
    'acceso_lista_asigna : tipo_var accesos IGUAL ARRAY PARIZQ PARDER PTCOMA'
    t[0] = AccesoLista(t[1],t[2],t[4],t.slice[3].lineno,1,True)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('acceso_lista_asigna ->  tipo_var accesos IGUAL ARRAY PARIZQ PARDER PTCOMA','acceso_lista_asigna.inst = AccesoLista(tipovar.val,accesos.lista,new Array());',lista)
    func(0,gramatical)

def  p_accesos(t):
    'accesos :  accesos acceso'
    t[1].append(t[2])
    t[0] = t[1]
    gramatical = G.ValorAscendente('accesos -> accesos acceso','accesos.lista = accesos1.lista; </hr> accesos.lista.add(acceso.val);',[])
    func(2,gramatical)

def  p_accesos_u(t):
    'accesos :  acceso'
    t[0] = [t[1]]
    gramatical = G.ValorAscendente('accesos -> acceso','accesos.lista = [acceso.val];',[])
    func(2,gramatical)

def  p_acceso(t):
    'acceso : CORIZQ primitiva CORDER'
    t[0] = t[2]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('acceso -> CORIZQ primitiva CORDER','acceso.val = primitiva.val;',lista)
    func(0,gramatical)

def p_error(t):
    try:
        error = Error.Error("SINTACTICO","Error sintactico, no se esperaba el valor "+t.value,t.lineno,find_column(t))
        ReporteErrores.func(error)
    except:
        error = Error.Error("SINTACTICO","Error sintactico",1,1)
        ReporteErrores.func(error)
    

parser = yacc.yacc()

def parse(input) :
    global lexer
    input = input.replace("\r","")
    lexer = lex.lex()
    return parser.parse(input)