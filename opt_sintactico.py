import ply.yacc as yacc
from opt_lexico import fighting, tokens
from sys import stdin

from objetos import NodoError, Exporte
import opt_sentencias as exp

global traduccion
traduccion = ""
global listaErrores
listaErrores = []
global contaerrores
contaerrores = 0
arbol = []

listaexp =[]
listafinal = []

#precedencia
precedence = (
    ('left','mas','menos'),
    ('left','asterisco','dividido'),
    ('left', 'modulo'),
    ('left', 'and', 'or'),
    ('left','mayorque','mayoriwal', 'menorque', 'menoriwal', 'iwaliwal', 'distintoque'),
    ('left', 'parentesisa', 'parentesisc'),    
)

#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------
def p_inicio(t):
    '''INICIO : INSTRUCCIONES'''
    t[0] = t[1]

def p_instrucciones(t):
    '''INSTRUCCIONES : INSTRUCCIONES INSTRUCCION  '''

def p_instrucciones2(t):
    '''INSTRUCCIONES :  INSTRUCCION '''

def p_instruccion(t):
    '''INSTRUCCION  :  INICIOSALTO
                    | INICIOGOTO
                    | CREARIF
                    | ASIGNACION
                    | IMPRESION
                    | LLAMADAMETODO
                    | METODO'''

def p_inicioSalto(t): 
    ''' INICIOSALTO : salto dospuntos '''
    t[0] = t[1] + t[2] 
    listaexp.append(exp.InicioSalto(t[1], t[0] ))

def p_inicioGoto(t): 
    ''' INICIOGOTO : goto salto puntocoma '''
    t[0] = t[1] + " " + t[2] + t[3]
    listaexp.append(exp.InicioGoto(t[2], t[0]))

def p_crearIf(t): 
    ''' CREARIF : if parentesisa IZQ SIMBOLO IZQ parentesisc llavesa goto salto llavesc  '''
    t[0] = t[1] + t[2] + t[3] + t[4] + t[5] + t[6] + t[7] + t[8] + " " + t[9] + t[10]
    listaexp.append(exp.InicioIf(exp.Comparacion(t[3], t[4], t[5], t[3] + t[4] + t[5]), t[9], t[0]))

def p_asignacion(t):
    '''ASIGNACION : LADO igual LADO puntocoma'''
    t[0] = t[1] + t[2] + t[3] +t[4]
    listaexp.append(exp.Asignacion(t[1], t[3], t[0]))

def p_impresion(t):
    ''' IMPRESION : fmt punto printf parentesisa TIPOCHAR coma ICHAR parentesisc puntocoma'''
    t[0] = t[1] + t[2] + t[3] + t[4] + "\"" + t[5] + "\"" + t[6] + t[7] + t[8] + t[9]
    listaexp.append(exp.Impresion(t[5], t[7], t[0]))

def p_llamadametodo(t):
    '''LLAMADAMETODO : id parentesisa parentesisc puntocoma'''
    t[0] = t[1] + t[2] + t[3] + t[4]
    listaexp.append(exp.LlamadaMetodo(t[1], t[0]))

def p_metodo(t):
    '''METODO : func id parentesisa parentesisc llavesa INSTRUCCIONES return puntocoma llavesc'''
    global listaexp
    global listafinal
    x = exp.Metodo(t[2], listaexp)
    listafinal.append(x)
    listaexp = []

def p_metodo2(t):
    '''METODO : func main parentesisa parentesisc llavesa INSTRUCCIONES llavesc '''
    global listaexp
    global listafinal
    x = exp.Metodo(t[2], listaexp)
    listafinal.append(x)
    listaexp= []



#  ----------------------------------------- OTROS --------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_ichar(t):
    '''ICHAR : int parentesisa DER parentesisc '''
    t[0] = t[1] + t[2] + t[3] + t[4]

def p_ichar2(t):
    '''ICHAR : IZQ'''
    t[0] = t[1]

def p_tipochar(t):
    '''TIPOCHAR : impc
            | impd
            | impf'''
    t[0] = t[1]

def p_lado(t):
    '''LADO : OPERACION
            | GETSTACK
            | GETHEAP
            | DER'''
    t[0] = t[1]

def p_operacion(t):
    '''OPERACION : DER OP DER'''
    t[0] = t[1] + t[2] + t[3]

def p_der(t):
    '''DER : IZQ
            | h
            | p'''
    t[0] = t[1]

def p_getstack(t):
    '''GETSTACK : stack corchetea int parentesisa DER parentesisc corchetec'''
    t[0] = t[1] + t[2] + t[3] + t[4] + str(t[5]) + t[6] +t[7]

def p_getheap(t):
    '''GETHEAP : heap corchetea int parentesisa DER parentesisc corchetec'''
    t[0] = t[1] + t[2] + t[3] + t[4] + str(t[5]) + t[6] +t[7]

def p_izq(t):
    '''IZQ : int
            | temporal
            | flotante
            | NEG'''
    t[0] = str(t[1])

def p_simbolo(t):
    '''SIMBOLO : mayorque
            | menorque
            | mayoriwal
            | menoriwal
            | iwaliwal
            | distintoque
            | and
            | or'''
    t[0] = t[1]

def p_op(t):
    '''OP : mas
        | menos
        | asterisco
        | dividido
        | modulo'''
    t[0] = t[1]

def p_neg(t):
    '''NEG : menos int
        | menos flotante'''
    t[0] = t[1] + str(t[2])

#  ----------------------------------------- FUNCSS --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def opt_sintactico(texto):

    global listafinal
    listafinal = []

    fighting(texto)
    parser = yacc.yacc()
    result = parser.parse(texto)
    print(result)
    print('--------------------------------------------------------------------------------------------')
    
    print(listafinal)
    
    return listafinal


mitexto = '''func imprimir() {
t1 = P+1;
t2 = stack[int(t1)];
L0:
t3 = heap[int(t2)];

if(t3 == -1) {goto L1}

fmt.Printf(\"%c\", int(t3));
t2 = t2+1;
goto L0;

L1:
return;

}
func main() {
P = 0; H = 0;

stack[int(0)] = 1;

stack[int(1)] = 10;
}'''
#fighting2(mitexto)