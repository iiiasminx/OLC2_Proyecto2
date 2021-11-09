# ----------------------------------------------------------------------------------------------------- 
#-------------------------------- INICIO LÉXICO OPTIMIZADOR -------------------------------------------
# -----------------------------------------------------------------------------------------------------

import ply.lex as lex
from objetos import NodoError

contaerrores = 0
listaErrores = []

reservadas = {    
    # impresion
    'println', 'fmt', 'printf',
    #reservadas
    'if', 'goto', 'return', 
    # tiempo de ejecución
    'stack', 'heap', 'p', 'h', 
    # funciones
    'func', 'main', 
    #tipos 
    'int', 'float64',
}

tokens = [
    'tab',
    # impresion 
    'impd', 'impc', 'impf' ,

    # agrupadores
    'corchetea', 'corchetec',
    'parentesisa', 'parentesisc',
    'llavesa', 'llavesc',
    #operaciones condicionales
    'mayorque',     'menorque',
    'mayoriwal',     'menoriwal',
    'iwaliwal',     'distintoque',
    # operaciones artiméticas
    'mas',     'menos',
    'asterisco',  'dividido',
    'modulo',  'igual',

    #variables
    'temporal', 'salto',
    'id', 'flotante', 'int'
    #otros
    'punto', 'dospuntos',
    'char', 'cadena', 'coma',
    'puntocoma',

    # condicionales x2
    'or',  'and',

    #comentario
    'comentario', 'cambiolinea', 'punto'
]+ list(reservadas)

t_ignore = r' '

t_println = r'fmt\.Printf'

# operadores
t_puntocoma = r';'
t_punto = r'\.'
t_dospuntos = r':'

t_corchetea = r'\['
t_corchetec = r'\]'
t_parentesisa = r'\('
t_parentesisc = r'\)'
t_llavesa = r'{'
t_llavesc = r'}'

t_mayorque = r'>'
t_menorque = r'<'
t_mayoriwal = r'>='
t_menoriwal = r'<='
t_iwaliwal = r'=='
t_distintoque = r'!='


t_coma = r'\,'
t_mas = r'\+'
t_menos = r'-'
t_asterisco = r'\*'  # este sirve para mas cosas, awas
t_dividido = r'/'
t_modulo = r'%'  # se llama modulo pero eso no se me va a quedar
t_igual = r'='

t_impd = r'\"%d\"'
t_impc = r'\"%c\"'
t_impf = r'\"%f\"'

t_or = r'\|\|'
t_and = r'\&\&'

#id o palabra reservada
def t_tab(t):
    r'\t'
    pass

def t_cambiolinea(t):
    r'\r*\n+'
    t.lineno += t.value.count("\n")

def t_temporal(t):
    r't[0-9]+'
    return t

def t_salto(t):
    r'L[0-9]+'
    return t

def t_id(t):
    r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    if t.value.lower() in reservadas: 
        t.type = t.value.lower()
    return t

def t_comment2(t):
    r'(//)(.)*(\n)'
    pass

def t_flotante(t):
    r'([0-9]+\.[0-9]+)'
    t.value = float(t.value)
    return t

def t_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_char(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    if t.value.lower() == "%c": 
        t.type = 'impc'
    if t.value.lower() == "%d": 
        t.type = 'impd'
    if t.value.lower() == "%f": 
        t.type = 'impf'
    
    return t 

def t_error(t):
    desc = 'Error léxico con \"' + t.value[0] + '\"'
    global contaerrores
    contaerrores = contaerrores+1
    error1 = NodoError(contaerrores, desc, t.lineno, t.lexpos)
    listaErrores.append(error1)
    t.lexer.skip(1)

# ----------------------------------------------------------------------------------------------------- 
#-------------------------------------------- EXPORTANDO ----------------------------------------------
# -----------------------------------------------------------------------------------------------------
def fighting(texto):
    global listaErrores
    listaErrores = []
    global contaerrores 
    contaerrores = 0

    print('Importado con éxito!')
    lexer = lex.lex()
    lexer.input(texto)

    while True:
        tok = lexer.token()
        if not tok : break
        print(tok)
    
    print(listaErrores)
    return listaErrores


#EXTRAS
fighting('stack[int(2)] = 2021.202;H=H+1;fmt.Printf??("%c", 10);')