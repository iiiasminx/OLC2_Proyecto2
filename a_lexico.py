# ----------------------------------------------------------------------------------------------------- 
#-------------------------------------------- INICIO LÉXICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------

import ply.lex as lex
from objetos import NodoError

contaerrores = 0
listaErrores = []

reservadas = {
    # reservadas
    'nothing',
    'true',
    'false',

    'struct',
    'mutable',

    'parse',
    'trunc',
    'typeof',

    'push',
    'pop',
    'length',

    'uppercase',
    'lowercase',
    'println',
    'print',
    'float',

    'log10',
    'log',
    'sin',
    'cos',
    'tan',
    'sqrt',

    'int64',
    'float64',
    'bool',
    'char',
    'string',

    'global',
    'local',

    'function',
    'end',

    'if',
    'elseif',
    'else',

    'while',

    'for',
    'in',

    'break',
    'continue',
    'return'
}


tokens = [
    # generales
    'tab',
    'id',
    'int',
    'flotante',
    'caracter',
    'cadena',
    'array',

    'comment1',
    'comment2',

    # operadores
    'puntocoma',
    'punto',

    'corchetea',
    'corchetec',

    'parentesisa',

    'parentesisc',
    'coma',
    'mas',
    'menos',
    'asterisco',  # este sirve para mas cosas, awas
    'dividido',
    'modulo',  # se llama modulo pero eso no se me va a quedar
    'igual',
    'elevado',

    'mayorque',
    'menorque',
    'mayoriwal',
    'menoriwal',
    'iwaliwal',
    'distintoque',

    'or',
    'and',
    'not',
    'interrogacionc',

    'dolar',

    'dos_dospuntos',
    'dospuntos',
    'salto',
    'push2'
] + list(reservadas)


t_ignore = r' '
# operadores
t_puntocoma = r';'
t_punto = r'\.'

t_corchetea = r'\['
t_corchetec = r'\]'

t_parentesisa = r'\('
t_parentesisc = r'\)'

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
t_elevado = r'\^'

t_or = r'\|\|'
t_and = r'\&\&'
t_not = r'!'

t_interrogacionc = r'\?'


t_dos_dospuntos = r'::'
t_dospuntos = r':'
push2 = r'push\!'

def t_id(t):
    r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    if t.value.lower() in reservadas: #VER ESTO, PORQUE ES CASE SENSITIVE
        #t.value = t.value.upper()
        t.type = t.value.lower()
        #t.value = t.value.lower()
    return t
    

def t_comment1(t):
    r'(\#=).*\n*.*(=\#)'
    pass

def t_tab(t):
    r'\t'
    pass

def t_salto(t):
    r'\r*\n+'
    t.lineno += t.value.count("\n")
    #return t

def t_comment2(t):
    r'(\#)(.)*(\n)'
    pass

def t_flotante(t):
    r'([0-9]+\.[0-9]+)'
    t.value = float(t.value)
    return t

def t_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_caracter(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
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

    #while True:
    #    tok = lexer.token()
    #    if not tok : break
    #    print(tok)
    
    return listaErrores


#EXTRAS
#fighting('println if else while Ana MariA dEl MoNtE true')
