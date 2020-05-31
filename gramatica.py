# Definición de la gramática
from ast.Instruccion import Instruccion
from ValorImplicito.Operacion import Operacion
from ValorImplicito.Operacion import TIPO_OPERACION
from ValorImplicito.Primitivo import Primitivo
from  Primitivas.Imprimir import Imprimir

reservadas = {
    'int' : 'INT',
    'double' : 'DOUBLE',
    'string' : 'STRING',
    'boolean' : 'BOOL',
    'true'    : 'TRUE',
    'false'   : 'FALSE',
    'print' : 'IMPRIMIR',
    'while' : 'MIENTRAS',
    'if' : 'IF',
    'else' : 'ELSE'
}

tokens  = [
    'PTCOMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'RESTO',
    'POTENCIA',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_RESTO     = r'%'
t_POTENCIA  = r'\^'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
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
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','RESTO',"POTENCIA"),
    ('right','UMENOS'),
    )


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
    '''instruccion      : imprimir_instr'''
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3])

def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_unaria '''
    t[0] = t[1]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

#********************************************** OPERACIONES RELACIONALES ***********************************

#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS expresion %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.lexer.lineno,0)
    t[0] = op
#********************************************** OPERACIONES ARITMETICAS ***********************************
def p_expresion_numerica(t):
    '''expresion_numerica   :   expresion MAS expresion 
                            |   expresion MENOS expresion 
                            |   expresion POR expresion
                            |   expresion DIVIDIDO expresion
                            |   expresion RESTO expresion 
                            |   expresion POTENCIA expresion '''
    
    op = Operacion()
    if(t.slice[2].type == 'MAS'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.SUMA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MENOS'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.RESTA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'POR'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.DIVISION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'RESTO'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.MODULO,t.lexer.lineno,0)
    elif(t.slice[2].type == 'POTENCIA'):
        op.OperacionAritmetica(t[1],t[3],TIPO_OPERACION.POTENCIA,t.lexer.lineno,0)    

    t[0] = op
#********************************************** EXPRESIONES PRIMITIVAS ***********************************
def p_expresion_primitiva(t):
    '''primitiva : ENTERO
                 | DECIMAL
                 | CADENA
                 | TRUE
                 | FALSE '''
    op = Operacion()
    if(t.slice[1].type == 'CADENA'):
        op.Operacion(Primitivo(str(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'DECIMAL'):
        op.Operacion(Primitivo(float(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'ENTERO'):
        op.Operacion(Primitivo(int(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'TRUE'):
        op.Operacion(Primitivo(True,t.lexer.lineno,0))
    elif(t.slice[1].type == 'FALSE'):
        op.Operacion(Primitivo(False,t.lexer.lineno,0))

    t[0] = op

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)