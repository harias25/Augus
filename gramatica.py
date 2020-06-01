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
    'MEIQUE',
    'MAIQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'AND',
    'OR',
    'NOT'

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
t_MEIQUE    = r'<='
t_MAIQUE    = r'>='
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_RESTO     = r'%'
t_POTENCIA  = r'\^'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'!'

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
    ('left','OR','MENOS'),
    ('left','AND','MENOS'),
    ('nonassoc','MENQUE','MAYQUE','MEIQUE','MAIQUE','IGUALQUE','NIGUALQUE'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','RESTO',"POTENCIA"),
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
    '''instruccion      : imprimir_instr
                        | declaracion 
                        | asignacion 
                        | if_instruccion '''
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3])

def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_unaria 
                 | expresion_relacional 
                 | expresion_logica '''
    t[0] = t[1]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

#********************************************** IF - ELSE IF - ELSE *********************************************
def p_if(t):
    'if_instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[3],t[6],None,None,t.lexer.lineno,0)
def p_ifelse(t):
    'if_instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[3],t[6],t[10],None,t.lexer.lineno,0)
def p_ifelseif(t):
    'if_instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif '
    t[0] = If(t[3],t[6],None,t[8],t.lexer.lineno,0)

def p_ifelseifelse(t):
    'if_instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[3],t[6],t[11],t[8],t.lexer.lineno,0)

def p_leseif(t) :
    'lelseif    : lelseif elseif'
    t[1].append(t[2])
    t[0] = t[1]

def p_leseifI(t) :
    'lelseif    : elseif '
    t[0] = [t[1]]

def p_elseif(t):
    'elseif : ELSE IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[4],t[7],None,None,t.lexer.lineno,0)
#********************************************** ASIGNACIONES *********************************************
def p_asignacion(t):
    'asignacion : ID IGUAL expresion PTCOMA '
    t[0] = Asignacion(t[1],t[3],t.lexer.lineno,0)
#********************************************** DECLARACIONES *********************************************
def p_declaracion(t):
    'declaracion : tipo_dato ID PTCOMA '
    t[0] = Declaracion(t[2],t[1],None,t.lexer.lineno,0)

def p_declaracion2(t):
    'declaracion : tipo_dato ID IGUAL expresion PTCOMA '
    t[0] = Declaracion(t[2],t[1],t[4],t.lexer.lineno,0)


def p_tipo_dato(t):
    '''tipo_dato : INT 
            | DOUBLE
            | STRING
            | BOOL '''
    if t.slice[1].type == 'INT': t[0] = Tipo.ENTERO
    elif t.slice[1].type == 'DOUBLE': t[0] = Tipo.DOOBLE
    elif t.slice[1].type == 'STRING': t[0] = Tipo.STRING
    elif t.slice[1].type == 'BOOL': t[0] = Tipo.BOOLEAN

#********************************************** OPERACIONES RELACIONALES ***********************************
def p_expresion_relacional(t):
    '''expresion_relacional :   expresion MENQUE expresion 
                            |   expresion MAYQUE expresion 
                            |   expresion MEIQUE expresion
                            |   expresion MAIQUE expresion
                            |   expresion IGUALQUE expresion 
                            |   expresion NIGUALQUE expresion '''
    
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
#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS expresion %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.lexer.lineno,0)
    t[0] = op
#********************************************** OPERACIONES LOGICAS ***********************************
def p_expresion_logica(t):
    '''expresion_logica   : expresion AND expresion 
                          | expresion OR expresion'''
                          
    op = Operacion()
    if(t.slice[2].type == 'AND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.AND,t.lexer.lineno,0)
    elif(t.slice[2].type == 'OR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.OR,t.lexer.lineno,0)
    t[0] = op

def p_expresion_negacion(t):
    'expresion_logica   :   NOT expresion %prec NOT' 
    op = Operacion()
    op.OperacionNot(t[2],t.lexer.lineno,0)
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
        op.Operacion(t[1],t[3],TIPO_OPERACION.SUMA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.RESTA,t.lexer.lineno,0)
    elif(t.slice[2].type == 'POR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIVISION,t.lexer.lineno,0)
    elif(t.slice[2].type == 'RESTO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MODULO,t.lexer.lineno,0)
    elif(t.slice[2].type == 'POTENCIA'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.POTENCIA,t.lexer.lineno,0)    

    t[0] = op
#********************************************** EXPRESIONES PRIMITIVAS ***********************************
def p_expresion_primitiva(t):
    '''primitiva : ENTERO
                 | DECIMAL
                 | CADENA
                 | TRUE
                 | FALSE 
                 | ID '''

    op = Operacion()
    if(t.slice[1].type == 'CADENA'):
        op.Primitivo(Primitivo(str(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'DECIMAL'):
        op.Primitivo(Primitivo(float(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'ENTERO'):
        op.Primitivo(Primitivo(int(t[1]),t.lexer.lineno,0))
    elif(t.slice[1].type == 'TRUE'):
        op.Primitivo(Primitivo(True,t.lexer.lineno,0))
    elif(t.slice[1].type == 'FALSE'):
        op.Primitivo(Primitivo(False,t.lexer.lineno,0))
    elif(t.slice[1].type == 'ID'):
        op.Indentficador(t[1],t.lexer.lineno,0)

    t[0] = op

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)