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
from  Primitivas.Imprimir import Imprimir
from  Primitivas.Unset import Unset
from  Primitivas.Exit import Exit
from  Condicionales.If import If
import ply.yacc as yacc
import Reporteria.Error as Error
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
t_ignore = " \t"

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

def p_etiquetas(t) :
    'etiquetas    : etiqueta '
    t[0] = [t[1]]

def p_empty(t) :
    'empty :'
    t[0] = []

def p_etiqueta(t) :
    'etiqueta    : ID DOSP instrucciones '
    t[0] = Etiqueta(t[1],t[3],t.lexer.lineno,find_column(t.slice[1]))

def p_etiqueta_e(t) :
    'etiqueta    : ID DOSP empty '
    t[0] = Etiqueta(t[1],t[3],t.lexer.lineno,find_column(t.slice[1]))    
    

#********************************************** INSTRUCCIONES  ***********************************

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

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
                        | error '''
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ tipo_var PARDER PTCOMA'
    op = Operacion()
    op.Indentficador(t[3],t.lexer.lineno,find_column(t.slice[2]))
    t[0] =Imprimir(op)

def p_instruccion_imprimir_acceso(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ acceso_lista PARDER PTCOMA'
    t[0] =Imprimir(t[3])

def p_instruccion_imprimir_cadena(t) :
    '''imprimir_instr     : IMPRIMIR PARIZQ CADENA  PARDER PTCOMA
                          | IMPRIMIR PARIZQ CADENA2 PARDER PTCOMA'''
    op = Operacion()
    op.Primitivo(Primitivo("\n",t.lexer.lineno,0))
    t[0] = Imprimir(op)

def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_relacional
                 | expresion_unaria
                 | expresion_logica 
                 | expresion_bit_bit
                 | absoluto'''
    t[0] = t[1]

#********************************************** INSTRUCCIONES PRIMITIVAS ***********************************
def p_go_to(t):
    'go_to : GOTO ID PTCOMA'
    t[0] = GoTo(t[2],t.lexer.lineno,find_column(t.slice[1]))

def p_if(t):
    'if_instruccion : IF PARIZQ expresion PARDER go_to '
    t[0] = If(t[3],t[5],t.lexer.lineno,find_column(t.slice[1]))

def p_exit(t):
    'exit : EXIT PTCOMA'
    t[0] = Exit(t.lexer.lineno,find_column(t.slice[1]))

def p_unset(t):
    '''unset : UNSET PARIZQ TEMP PARDER PTCOMA
             | UNSET PARIZQ PARAM PARDER PTCOMA
             | UNSET PARIZQ RET PARDER PTCOMA
             | UNSET PARIZQ PILA PARDER PTCOMA'''
    t[0] = Unset(t[3],t.lexer.lineno,find_column(t.slice[1]))

#********************************************** ASIGNACIONES *********************************************
def p_asignacion(t):
    'asignacion : tipo_var IGUAL expresion PTCOMA '
    t[0] = Asignacion(t[1],t[3],t.lexer.lineno,1,False)

def p_asingacion_array(t):
    'asignacion : tipo_var IGUAL ARRAY PARIZQ PARDER PTCOMA '
    t[0] = Asignacion(t[1],{},t.lexer.lineno,1,False)

def p_puntero(t):
    'puntero : tipo_var IGUAL PAND  tipo_var PTCOMA '
    op = Operacion()
    op.Indentficador(t[4],t.lexer.lineno,find_column(t.slice[3])+1)
    t[0] = Asignacion(t[1],op,t.lexer.lineno,1,True)

def p_conversiones(t):
    'conversion : tipo_var IGUAL PARIZQ tipo_dato PARDER primitiva PTCOMA '
    t[0] = Conversion(t[1],t[6],t[4],t.lexer.lineno,1)


def p_tipo_dato(t):
    '''tipo_dato : INT 
                | FLOAT 
                | CHAR '''
    t[0] = t[1]

def p_tipo_var(t):
    '''tipo_var : TEMP 
                | PARAM 
                | RET 
                | PILA 
                | RA
                | PUNTERO '''
    t[0] = t[1]
#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS primitiva %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.lexer.lineno,find_column(t.slice[1]))
    t[0] = op
#********************************************** OPERACIONES LOGICAS ***********************************
def p_expresion_logica(t):
    '''expresion_logica   : primitiva AND primitiva 
                          | primitiva OR primitiva
                          | primitiva XOR primitiva '''
                          
    op = Operacion()
    if(t.slice[2].type == 'AND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.AND,t.lexer.lineno,1)
    elif(t.slice[2].type == 'OR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.OR,t.lexer.lineno,1)
    elif(t.slice[2].type == 'XOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XOR,t.lexer.lineno,1)
    t[0] = op

def p_expresion_negacion(t):
    'expresion_logica   :   NOT primitiva %prec NOT' 
    op = Operacion()
    op.OperacionNot(t[2],t.lexer.lineno,find_column(t.slice[1]))
    t[0] = op    

#********************************************** OPERACIONES BIT A BIT ***********************************
def p_expresion_bit_bit(t):
    '''expresion_bit_bit  : primitiva PAND primitiva 
                          | primitiva BOR primitiva
                          | primitiva XORR primitiva 
                          | primitiva SHIFTI primitiva
                          | primitiva SHIFTD primitiva'''
                          
    op = Operacion()
    if(t.slice[2].type == 'PAND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.PAND,t.lexer.lineno,1)
    elif(t.slice[2].type == 'BOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.BOR,t.lexer.lineno,1)
    elif(t.slice[2].type == 'XORR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XORR,t.lexer.lineno,1)
    elif(t.slice[2].type == 'SHIFTI'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTI,t.lexer.lineno,1)
    elif(t.slice[2].type == 'SHIFTD'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTD,t.lexer.lineno,1)

    t[0] = op

def p_expresion_negacion_bit(t):
    'expresion_bit_bit   :   NOTR primitiva %prec NOTR' 
    op = Operacion()
    op.OperacionNotBit(t[2],t.lexer.lineno,find_column(t.slice[1]))
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
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_QUE,t.lexer.lineno,1)
    elif(t.slice[2].type == 'MAYQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_QUE,t.lexer.lineno,1)
    elif(t.slice[2].type == 'MEIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_IGUA_QUE,t.lexer.lineno,1)
    elif(t.slice[2].type == 'MAIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_IGUA_QUE,t.lexer.lineno,1)
    elif(t.slice[2].type == 'IGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.IGUAL_IGUAL,t.lexer.lineno,1)
    elif(t.slice[2].type == 'NIGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIFERENTE_QUE,t.lexer.lineno,1)    

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
        op.Operacion(t[1],t[3],TIPO_OPERACION.SUMA,t.lexer.lineno,1)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.RESTA,t.lexer.lineno,1)
    elif(t.slice[2].type == 'POR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.lexer.lineno,1)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIVISION,t.lexer.lineno,1)
    elif(t.slice[2].type == 'RESTO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MODULO,t.lexer.lineno,1)
    t[0] = op

#********************************************** EXPRESIONES PRIMITIVAS ***********************************

def p_absoluto(t):
    'absoluto : ABS PARIZQ primitiva PARDER '
    op = Operacion()
    op.ValorAbsoluto(t[3],t.lexer.lineno,find_column(t.slice[1]))
    t[0] = op

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
        op.Primitivo(Primitivo(str(t[1]),t.lexer.lineno,find_column(t.slice[1])))
    elif(t.slice[1].type == 'DECIMAL'):
        op.Primitivo(Primitivo(float(t[1]),t.lexer.lineno,find_column(t.slice[1])))
    elif(t.slice[1].type == 'ENTERO'):
        op.Primitivo(Primitivo(int(t[1]),t.lexer.lineno,find_column(t.slice[1])))
    elif(t.slice[1].type == 'TEMP') or (t.slice[1].type == 'PARAM') or (t.slice[1].type == 'RET') or (t.slice[1].type == 'PILA') or (t.slice[1].type == 'RA') or (t.slice[1].type == 'PUNTERO'):
        op.Indentficador(t[1],t.lexer.lineno,find_column(t.slice[1]))
    elif(t.slice[1].type == 'acceso_lista'):
        op.AccesoLista(t[1],t.lexer.lineno,1)
    t[0] = op

#********************************************** LISTAS *******************************************
def  p_acceso_lista(t):
    'acceso_lista : tipo_var accesos'
    t[0] = AccesoLista(t[1],t[2],None,t.lexer.lineno,1,False)

def  p_acceso_lista_asigna(t):
    'acceso_lista_asigna : tipo_var accesos IGUAL expresion PTCOMA'
    t[0] = AccesoLista(t[1],t[2],t[4],t.lexer.lineno,1,False)

def  p_acceso_lista_asigna_array(t):
    'acceso_lista_asigna : tipo_var accesos IGUAL ARRAY PARIZQ PARDER PTCOMA'
    t[0] = AccesoLista(t[1],t[2],t[4],t.lexer.lineno,1,True)

def  p_accesos(t):
    'accesos :  accesos acceso'
    t[1].append(t[2])
    t[0] = t[1]

def  p_accesos_u(t):
    'accesos :  acceso'
    t[0] = [t[1]]

def  p_acceso(t):
    'acceso : CORIZQ primitiva CORDER'
    t[0] = t[2]

def p_error(t):
    error = Error.Error("SINTACTICO","Error sintactico, no se esperaba el valor "+t.value,t.lexer.lineno,find_column(t))
    ReporteErrores.func(error)

parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)