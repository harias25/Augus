# Definición de la gramática
from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.Operacion import Operacion
from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Operacion import TIPO_OPERACION
from ValorImplicito.Primitivo import Primitivo
from  Primitivas.Imprimir import Imprimir
from  Condicionales.If import If

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
	'$ra'	: 'RA',
	#'$sp'	: 'PILA',
	'xor'	: 'XOR'
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
     r'[$tT][0-9]+'
     t.type = reservadas.get(t.value.lower(),'TEMP')    # Check for reserved words
     return t

def t_PARAM(t):
     r'[$aA][0-9]+'
     t.type = reservadas.get(t.value.lower(),'PARAM')    # Check for reserved words
     return t

def t_RET(t):
     r'[$vV][0-9]+'
     t.type = reservadas.get(t.value.lower(),'RET')    # Check for reserved words
     return t

def t_PILA(t):
     r'[$sS][0-9]+'
     t.type = reservadas.get(t.value.lower(),'PILA')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


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
    ('right','UMENOS','NOT'),
    )

#precedence nonassoc menor,mayor, menor_igual,mayor_igual;

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : imprimir_instr '''
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3])

def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_relacional
                 | expresion_unaria
                 | expresion_logica '''
    t[0] = t[1]

#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS primitiva %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.lexer.lineno,0)
    t[0] = op
#********************************************** OPERACIONES LOGICAS ***********************************
def p_expresion_logica(t):
    '''expresion_logica   : primitiva AND primitiva 
                          | primitiva OR primitiva'''
                          
    op = Operacion()
    if(t.slice[2].type == 'AND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.AND,t.lexer.lineno,0)
    elif(t.slice[2].type == 'OR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.OR,t.lexer.lineno,0)
    t[0] = op

def p_expresion_negacion(t):
    'expresion_logica   :   NOT primitiva %prec NOT' 
    op = Operacion()
    op.OperacionNot(t[2],t.lexer.lineno,0)
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
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_QUE,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MAYQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_QUE,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MEIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_IGUA_QUE,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MAIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_IGUA_QUE,t.lexer.lineno,0)
    elif(t.slice[2].type == 'IGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.IGUAL_IGUAL,t.lexer.lineno,0)
    elif(t.slice[2].type == 'NIGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIFERENTE_QUE,t.lexer.lineno,0)    

    t[0] = op
#********************************************** OPERACIONES ARITMETICAS ***********************************
def p_expresion_numerica(t):
    '''expresion_numerica   :   primitiva MAS primitiva 
                            |   primitiva MENOS primitiva 
                            |   primitiva POR primitiva
                            |   primitiva DIVIDIDO primitiva
                            |   primitiva RESTO primitiva '''

    op = Operacion()
    if(t.slice[2].type == 'MAS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SUMA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.RESTA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'POR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIVISION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'RESTO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MODULO,t.lexer.lineno,0)   
    t[0] = op
#********************************************** EXPRESIONES PRIMITIVAS ***********************************
def p_expresion_primitiva(t):
    '''primitiva : ENTERO
                 | DECIMAL
                 | CADENA
                 | TEMP '''
    op = Operacion()
    if(t.slice[1].type == 'CADENA'):
        op.Primitivo(Primitivo(str(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'DECIMAL'):
        op.Primitivo(Primitivo(float(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'ENTERO'):
        op.Primitivo(Primitivo(int(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'TEMP'):
        op.Indentficador(t[1],t.lexer.lineno,0)
    t[0] = op

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)