# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
from a_lexico import fighting, tokens
from sys import stdin

from operaciones import *
from instrucciones import *
from objetos import NodoError, Exporte

global traduccion
traduccion = ""
global listaErrores
listaErrores = []
global contaerrores
contaerrores = 0
arbol = []


#precedencia
precedence = (
    ('left','mas','menos'),
    ('left','asterisco','dividido'),
    ('left', 'elevado', 'modulo'),
    ('left','umenos'), #sujeto a cambios
    ('left', 'and', 'or'),
    ('left','not'),
    ('left','mayorque','mayoriwal', 'menorque', 'menoriwal', 'iwaliwal', 'distintoque'),
    ('left', 'parentesisa', 'parentesisc'),    
    )

#expresiones

#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------
def p_inicio(t):
    '''INICIO : INSTRUCCIONES2'''
    t[0] = t[1]
    global arbol
    arbol = t[0] #el arbol es un array de instrucciones

def p_instrucciones2(t):
    '''INSTRUCCIONES2 : INSTRUCCIONES2 INSTRUCCION2 puntocoma '''
    t[1].append(t[2])
    t[0] = t[1]
    #print('Instrucciones2', t[0]) 

def p_instrucciones21(t):
    '''INSTRUCCIONES2 :  INSTRUCCION2 puntocoma'''
    t[0] = [t[1]]
    #print('Instrucciones2II', t[0])

def p_instruccion2(t):
    '''INSTRUCCION2  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | SOPERACIONES
                    | TYPESTRUCT'''  
    t[0] = t[1] 
    #print('Instruccion2', t[0])

#LO QUE VA ADENTRO DEL TEXTO
def p_instrucciones1(t):
    '''INSTRUCCIONES : INSTRUCCIONES INSTRUCCION puntocoma '''
    t[1].append(t[2])
    t[0] = t[1]
    
def p_instrucciones11(t):
    '''INSTRUCCIONES :  INSTRUCCION puntocoma'''
    t[0] = [t[1]]
    

def p_instruccion(t):
    '''INSTRUCCION  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | SOPERACIONES
                    | TYPESTRUCT'''
    t[0] = t[1]

def p_soperaciones(t):
    '''SOPERACIONES : SOPSTRING
                    | SOPNATIV
                    | OPID
                    | SOPLOG
                    | DECLNATIV'''
    t[0] = t[1]
#  ----------------------------------------TIPOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_tipos(t):
    '''TIPOS : int64
            | float64
            | bool
            | char
            | string'''    
    t[0] = OPType(t[1])
    
def p_tipos2(t):
    '''TIPOS :  id'''
    t[0] = OPType(OPID(t[1]))   
    
def p_algo(t):
    '''ALGO : SOPERACIONES
            | ARREGLO
            | LLAMADARR
            | STRUCTINI'''
    t[0] = t[1]

def p_algo2(t):
    '''ALGO : id'''
    t[0] = OPID(t[1])
#  -------------------------------------- STRUCT------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_typestruct(t):
    '''TYPESTRUCT : STRUCT'''
    t[0] = t[1]
    
def p_typestruct2(t):
    '''TYPESTRUCT : mutable STRUCT'''
    t[2].tipo = 1
    t[0] = t[2]

def p_struct(t):
    '''STRUCT : struct id ATRIBUTOS end'''
    t[0] = DeclStruct(t[2], t[3])

def p_atributos(t):
    '''ATRIBUTOS : ATRIBUTOS ATRIBUTO puntocoma '''
    t[1].append(t[2])
    t[0] = t[1]
    
def p_atributos2(t):
    '''ATRIBUTOS :  ATRIBUTO  puntocoma'''
    t[0] = [t[1]]
    
def p_atributo(t):
    '''ATRIBUTO : id dos_dospuntos TIPOS ''' 
    t[0] = OPAtributpTipado(t[1], t[3])
    
def p_atributo2(t):
    '''ATRIBUTO :  id ''' #quite el ; de acá
    t[0] = OPAtributo(t[1])
    
def p_creacionstruct(t):
    '''STRUCTINI : id parentesisa PARAMSFUNCS parentesisc'''
    t[0] = LlamadaFuncion(t[1], t[3])

def p_structasign(t):
    '''STRUCTASIGN : id ''' 
    t[0] = OPID(t[1])   

def p_structasign1(t):
    '''STRUCTASIGNS : STRUCTASIGNS punto STRUCTASIGN '''
    t[1].append(t[3])
    t[0] = t[1]

def p_structasign2(t):
    '''STRUCTASIGNS :  STRUCTASIGN'''
    t[0] = [t[1]]

#  ------------------------------------ ARREGLOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_arreglo(t):
    '''ARREGLO : corchetea ARRCONTS corchetec'''
    t[0] = t[2]   # sujeto a cambios

def p_arrcont(t):
    '''ARRCONTS : ARRCONTS coma ARRCONT '''
    t[1].append(t[3])
    t[0] = t[1]

def p_arrcont2(t):
    '''ARRCONTS :  ARRCONT '''
    t[0] = [t[1]]

def p_arrcont4(t):
    '''ARRCONT :  ALGO '''
    t[0] = t[1]

def p_arrcont3(t):
    '''ARRCONT :  '''
    t[0] = OPNothing()

def p_llamadaarr(t):
    '''LLAMADARR : id INDARS'''
    t[0] = LlamadaArr(t[1], t[2])

def p_indarcvzx(t):
    '''INDARS : INDARS  INDAR corchetec'''
    t[1].append(t[2]) #yo creo que esto me da los indices al revés :'v
    t[0] = t[1]     # de hecho si me los da bien!  :D
    
def p_indars2(t):
    '''INDARS : INDAR corchetec'''
    t[0] = [t[1]]
    
def p_indar2(t):
    '''INDAR : corchetea id'''
    t[0] = OPID(t[2])    
    
def p_indar(t):
    '''INDAR :  corchetea OPID '''
    t[0] = t[2]

#  ------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_declfunc(t):
    '''DECLFUNC : function id parentesisa PARAMS parentesisc INSTRUCCIONES end '''
    t[0] = DefFuncion(t[2], t[4], t[6])

def p_params(t):
    '''PARAMS : PARAMS coma PARAM '''
    t[1].append(t[3])
    t[0] = t[1]
    
def p_params4(t):
    '''PARAMS :  PARAM'''
    t[0] = [t[1]]

def p_params2(t):
    '''PARAM : id '''
    t[0] = DefFuncParam(OPID(t[1]))

def p_params5(t):
    '''PARAM :  '''
    t[0] = DefFuncParam(OPNothing())

def p_params3(t):
    '''PARAM : id dos_dospuntos TIPOS'''
    t[0] = DefFuncParam(OPID(t[1]), t[3])

def p_llamadafunc(t):
    '''LLAMADAFUNC : id parentesisa PARAMSFUNCS parentesisc'''
    t[0] = LlamadaFuncion(t[1], t[3])
    #print('llamadaFunc detectada')

def p_paramsfunc(t):
    '''PARAMSFUNCS : PARAMSFUNCS coma PARAMSFUNC'''
    t[1].append(t[3])
    t[0] = t[1]

def p_paramsfunc44(t):
    '''PARAMSFUNCS :  PARAMSFUNC'''
    t[0] = [t[1]]

def p_paramsfunc3(t):
    '''PARAMSFUNC :  ALGO'''    
    t[0] = t[1]

def p_paramsfunc2(t):
    '''PARAMSFUNC :  '''
    t[0] = OPNothing()
    
#  ---------------------------------ASIGNACIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sope(t):
    '''SCOPE : global ASIGNACION
            | local ASIGNACION
            | ASIGNACION'''
    if t[1] == 'global'  : 
        t[0] = Scope(t[2], t[1])
    elif t[1] == 'local'  : 
        t[0] = Scope(t[2], t[1])
    else:
        t[0] = Scope(t[1], 'local')

#cualquiera

def p_nombrealgo(t):
    '''NOMBREALGO : LLAMADARR
                | STRUCTASIGNS'''
    t[0] = t[1]
    
def p_nombrealgo2(t):
    '''NOMBREALGO : id'''
    t[0] = OPID(t[1])

#string

def p_asignaciones3(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING '''
    t[0] = Asignacion(t[1], t[3])

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING dos_dospuntos TIPOS '''
    t[0] = AsignacionTipada(t[1], t[3], t[5])

#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : NOMBREALGO igual ALGO '''
    t[0] = Asignacion(t[1], t[3])

def p_asignaciones2(t):
    '''ASIGNACION : NOMBREALGO igual ALGO dos_dospuntos TIPOS '''
    t[0] = AsignacionTipada(t[1], t[3], t[5])

#nothing

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual nothing '''
    t[0] = Asignacion(t[1], OPNothing())

def p_asignaciones5(t):
    '''ASIGNACION : NOMBREALGO  '''
    t[0] = t[1]

#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF
                | FWHILE
                | FFOR'''
    t[0] = t[1]

def p_transferencia(t):
    '''TRANSF : break 
            | continue 
            | return '''
    if t[1] == 'break' : t[0] = SBreak()
    elif t[1] == 'continue': t[0] = SContinue()
    else : t[0] = SReturn(OPNothing())

def p_transferencia2(t):
    '''TRANSF : return ALGO'''
    t[0] = SReturn(t[2])

#  -------------------------------------- FOR---------------------------------------------------------

def p_ffor(t):
    '''FFOR : for id in RANGO INSTRUCCIONES end'''
    t[0] = FFor(t[2], t[4], t[5])

def p_rangofor(t):
    '''RANGO : OPID dospuntos OPID'''
    t[0] = FForRangoNum(t[1], t[3])

def p_rangofor2(t):
    '''RANGO : cadena'''
    t[0] = OPCadena(t[1])

def p_rangofor4(t):
    '''RANGO : id'''
    t[0] = OPID(t[1])

def p_rangofor3(t):
    '''RANGO : ARREGLO'''
    t[0] = t[1]

#  ------------------------------------WHILE ---------------------------------------------------------

def p_fwhile(t):
    '''FWHILE : while SOPLOG INSTRUCCIONES end'''
    t[0] = FWhile(t[2], t[3])

#  -------------------------------------- IF ---------------------------------------------------------

def p_fif(t):
    '''FIF : if SOPLOG INSTRUCCIONES FELSEIF
            | if SOPLOG INSTRUCCIONES FELSE''' 
    t[0] = FIF(t[2], t[3], t[4])

def p_fif2(t):
    '''FIF :  if SOPLOG INSTRUCCIONES end'''
    t[0] = FIF(t[2], t[3], [OPPASS()]) 
    
def p_felseif(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES FELSEIF
            | elseif SOPLOG INSTRUCCIONES FELSE'''
    t[0] = FElseIF(t[2], t[3], t[4])

def p_felseif2(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES end'''
    t[0] = FElseIF(t[2], t[3], [OPPASS()])

def p_felse(t):
    '''FELSE : else INSTRUCCIONES end'''
    t[0] = FELSE(t[2])

def p_fifunilinea(t):
    ''' FIFUNI : SOPLOG interrogacionc ALGO dospuntos ALGO'''
    t[0] = FIFuni(t[1], t[3], t[5])

    
#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNTS parentesisc '''
    t[0] = Impresionln(t[3]) 

def p_sprint2(t):
    '''IMPRIMIR :  print parentesisa SCONTPRNTS parentesisc '''
    t[0] = Impresion(t[3]) 

def p_scontprint(t):
    '''SCONTPRNTS : SCONTPRNTS coma SCONTPRNT'''
    t[1].append(t[3])
    t[0] = t[1]

def p_scontprint2(t):
    '''SCONTPRNTS :  SCONTPRNT'''
    t[0] = [t[1]]

def p_scontprintterm(t):
    '''SCONTPRNT :  ALGO
                | FIFUNI
                | LLAMADAFUNC'''
    t[0] = t[1]

#  -------------------------------OPERACION CON ID ---------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def p_sopid3(t):
    '''OPID : OPID mas OPID
                    | OPID menos OPID
                    | OPID asterisco OPID
                    | OPID dividido OPID
                    | OPID modulo OPID
                    | OPID elevado OPID'''
    if t[2] == '+'  : t[0] = OPBinaria(t[1], ARITMETICA.MAS, t[3])
    elif t[2] == '-': t[0] = OPBinaria(t[1], ARITMETICA.MENOS, t[3])
    elif t[2] == '*': t[0] = OPBinaria(t[1], ARITMETICA.ASTERISCO, t[3])
    elif t[2] == '/': t[0] = OPBinaria(t[1], ARITMETICA.DIVIDIDO, t[3])
    elif t[2] == '%': t[0] = OPBinaria(t[1], ARITMETICA.MODULO, t[3])
    elif t[2] == '^': t[0] = OPBinaria(t[1], ARITMETICA.ELEVADO, t[3])

def p_sopid4(t):
    '''OPID : menos OPID %prec umenos'''
    t[0] = OPNeg(t[2])   
    

def p_sopid8(t):
    '''OPID : parentesisa OPID parentesisc'''
    t[0] = t[2]   
    

def p_sopid7(t):
    '''OPID : NATMATH parentesisa OPID parentesisc'''
    if t[1] == 'log10': t[0] = OPNativa(t[3], MATH.LOG10)
    elif t[1] == 'sin': t[0] =OPNativa(t[3], MATH.SIN)
    elif t[1] == 'cos': t[0] =OPNativa(t[3], MATH.COS)
    elif t[1] == 'tan': t[0] =OPNativa(t[3], MATH.TAN)
    elif t[1] == 'sqrt': t[0] =OPNativa(t[3], MATH.SQRT)
    
def p_sopid6(t):
    '''OPID : log parentesisa OPID coma OPID parentesisc'''
    t[0] = OPNativaLog(t[3], t[5])


def p_sopid5(t):
    '''OPID : int
            | flotante'''
    t[0] = OPNum(t[1])
    

def p_sopid9(t):
    '''OPID :  id    '''
    t[0] = OPID(t[1])
    

def p_sopid10(t):
    '''OPID : cadena
            | caracter'''
    t[0] = OPCadena(t[1])
    

def p_sopid11(t):
    '''OPID : LLAMADARR
            | LLAMADAFUNC
            | SOPNATIV'''
    t[0] = t[1]#
    


#------------------------------OPERACIONES LOGICAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_soplog(t):
    '''SOPLOG : SOPLOG and SOPLOG
            | SOPLOG or SOPLOG
            | SOPLOG mayorque SOPLOG
            | SOPLOG menorque SOPLOG
            | SOPLOG mayoriwal SOPLOG
            | SOPLOG menoriwal SOPLOG
            | SOPLOG iwaliwal SOPLOG
            | SOPLOG distintoque SOPLOG'''
    if t[2] == '&&'  : t[0] = OPLogica(t[1], LOGICA.AND, t[3])
    elif t[2] == '||': t[0] = OPLogica(t[1], LOGICA.OR, t[3])
    elif t[2] == '>': t[0] = OPLogica(t[1], LOGICA.MAYORQUE, t[3])
    elif t[2] == '<': t[0] = OPLogica(t[1], LOGICA.MENORQUE, t[3])
    elif t[2] == '>=': t[0] = OPLogica(t[1], LOGICA.MAYORIWAL, t[3])
    elif t[2] == '<=': t[0] = OPLogica(t[1], LOGICA.MENORIWAL, t[3])
    elif t[2] == '==': t[0] = OPLogica(t[1], LOGICA.IWAL, t[3])
    elif t[2] == '!=': t[0] = OPLogica(t[1], LOGICA.DISTINTO, t[3])

def p_soplogPar(t):
    '''SOPLOG : parentesisa SOPLOG parentesisc'''
    t[0] = t[2]

def p_soplogterm2(t):
    '''SOPLOG : OPID
            | LLAMADARR
            | SOPNATIV'''
    t[0] = t[1]
    
def p_soplogterm(t):
    '''SOPLOG : int
            | flotante''' 
    t[0] = OPNum(t[1])   

def p_soplogterm3(t):
    '''SOPLOG : cadena
            | caracter'''   
    t[0] = OPCadena(t[1]) 

def p_soplogterm4(t):
    '''SOPLOG : id'''  
    t[0] = OPID(t[1])  

def p_soplogterm(t):
    '''SOPLOG : true
            | false'''  
    t[0] = OPBool(t[1])  

#------------------------------OPERACIONES NATIVAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopnativ(t):
    '''SOPNATIV : uppercase parentesisa SOPN parentesisc
                | lowercase parentesisa SOPN parentesisc
                | length parentesisa SOPN parentesisc
                | pop parentesisa SOPN parentesisc'''
    if t[1] == 'uppercase' : t[0] = OPUppercase(t[3])
    elif t[1] == 'lowercase' : t[0] = OPLowercase(t[3])
    elif t[1] == 'pop' : t[0] = OPPop(t[3])
    else : t[0] = OPLength(t[3])


def p_sopnativterm(t):
    ''' SOPN :  SOPSTRING
            | ARREGLO
            | LLAMADARR''' 
    t[0] = t[1]

def p_soppush(t):
    '''SOPNATIV : push parentesisa SOPN coma ALGO parentesisc'''
    t[0] = OPPush(t[3], t[5])

def p_declnativ(t):
    '''DECLNATIV : parse parentesisa TIPOS coma ALGO parentesisc'''
    t[0] = FParse(t[3], t[5])

def p_declnativ2(t):
    '''DECLNATIV : trunc parentesisa int64 coma ALGO parentesisc'''
    t[0] = FTrunc(t[5])

def p_declnativ2(t):
    '''DECLNATIV : trunc parentesisa ALGO parentesisc'''
    t[0] = FTrunc(t[3])

def p_declnativ3(t):
    '''DECLNATIV :  float parentesisa ALGO parentesisc'''
    t[0] = FFloat(t[3])

def p_declnativ4(t):
    '''DECLNATIV :  string parentesisa ALGO parentesisc'''
    t[0] = FString(t[3])

def p_declnativ5(t):
    '''DECLNATIV : typeof parentesisa ALGO parentesisc'''
    t[0] = Ftypeof(t[3])

#------------------------------OPERACIONES STRING ----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopstring(t):
    '''SOPSTRING : SOPSTRING asterisco SOPSTRING'''
    t[0] = OPMergeString(t[1], t[3])


def p_sopstring2(t):
    '''SOPSTRING :  SOPSTRING elevado int'''
    t[0] = OPElevarString(t[1], OPNum(t[3]))

def p_sopstring3(t):
    '''SOPSTRING :  SOPSTRING elevado id'''

    t[0] = OPElevarString(t[1], OPID(t[3]))

def p_sopstringterm(t):
    '''SOPSTRING : cadena
                | caracter'''
    t[0] = OPCadena(t[1])

def p_sopstringterm3(t):
    '''SOPSTRING : id'''    
    t[0] = OPID(t[1])   

def p_sopstringterm2(t):
    '''SOPSTRING : SOPNATIV
                | DECLNATIV''' 
    t[0] = t[1]  

#  ----------------------------OPERACIONES NUMÉRICAS--------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def p_nathmath(t):
    '''NATMATH : log10
                | sin
                | cos
                | tan
                | sqrt '''
    t[0] = t[1]
    


#  --------------------------------------- ERRORES --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def p_error(t):
    try: 
        desc = 'Error sintactico con \"' + t.value + '\"'
        global contaerrores
        contaerrores = contaerrores+1
        error1 = NodoError(contaerrores, desc, t.lineno, t.lexpos)
        listaErrores.append(error1)
        
        print("Error sintactico en '%s'" % t.value)
    except Exception as e:
        print('Algo pasó en el error :c ', e)


#  ----------------------------------------- OTROS --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def fighting2(texto):
    #asignaciones iniciales
    global traduccion 
    traduccion = ''

    global listaErrores
    listaErrores = []
    global contaerrores
    contaerrores = 0

    #fighting(texto)
    parser = yacc.yacc()
    result = parser.parse(texto)
    print(result)

    global arbol
    exportacion = Exporte('', '', listaErrores, '', arbol)
    return exportacion


#fighting('uppercase()')

#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
