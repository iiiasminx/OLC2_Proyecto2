# importo todo de todos lados
from sys import exc_info
from a_lexico import fighting, tokens
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 
import math

arbol =[]

lista_simbolos = [] # acá van todos los valores que se hayan declarado
ts_global = cst.TablaSimbolos()
pilaentornos = []

contaerrores = 0
listasemanticos = []

contabucle = 0
extra = ""

contatemporales = 0
contasaltos = 0

traduccion = ""
traducciontemporal = ""

def compilando(texto):
    #print('Esto es lo que tengo que traducir', texto)
    global contatemporales
    contatemporales = 0
    global traduccion 
    global traducciontemporal
    traducciontemporal = ""  
    traduccion = """package main\nimport ("fmt")\n"""
    traduccion += "var stack [10000]float64\nvar heap [100000]float64\n"
    traduccion += "var P, H float64\n"

    # probando lexico
    lexicos = fighting(texto)

    #probando sintactico
    paquete = fighting2(texto)
    global arbol 
    arbol = paquete.arbol
    #metiendo encabezados
    procesarInstrucciones(arbol, ts_global)

    traduccion += "var "

    for i in range(contatemporales):
        if i == contatemporales-1:
            traduccion +=  "t" + str(i) + " float64\n\n"
        else:
            traduccion +=  "t" + str(i) + ", "

    traduccion += "func main() {\n\n"
    traduccion += traducciontemporal
    traduccion += "}"  

    

    paquete.traduccion = traduccion  
    paquete.errores_lexicos =lexicos

    return paquete

def procesarInstrucciones(ast, tablaSimbolos : cst.TablaSimbolos):
    contador = 1
    print('\n')
    global extra
    extra = ""

    for instruccion in ast:
        print(contador)
        contador += 1
        global contabucle
        contabucle = 0

        #OPERACIONES
        if extra != "" : return
        if isinstance(instruccion, Impresion): intImpresion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Impresionln): intImpresionLN(instruccion, tablaSimbolos)


# -------------------------------------------------------------------------
# IMPRESION ---------------------------------------------------------------
# -------------------------------------------------------------------------

def intImpresion(instr, tablaSimbolos: cst.TablaSimbolos):
    print('impresion')
    aux = ""
    for instruccion in instr.texto:
        # tal vez le tenga que poner un if al res, pero una crisis a la vez xd
        res = resolverNumerica(instruccion, tablaSimbolos)
        print('RESPUESTA: ', res)
        var = verificarT(res)
        txt = "\"%d\", int(" + var  + ")"
        if "." in str(res) or "t" in str(res): 
            txt = "\"%f\", " + var 
        aux += "fmt.Printf(" + txt + ");\n"   

    #aux += "fmt.Printf(\"%c\", 10);\n"
    meteraTraduccion(aux)    

def intImpresionLN(instr, tablaSimbolos : cst.TablaSimbolos):
    print('impresionLN')
    aux = ""
    for instruccion in instr.texto:
        # tal vez le tenga que poner un if al res, pero una crisis a la vez xd
        aux += "fmt.Printf(\"%c\", 10);\n"

        res = resolverNumerica(instruccion, tablaSimbolos)
        print('RESPUESTA: ', res)
        var = verificarT(res)
        txt = "\"%d\", int(" + var  + ")"
        if "." in str(res) or "t" in str(res): 
            txt = "\"%f\", " + var 
        aux += "fmt.Printf(" + txt + ");\n" 

        aux += "fmt.Printf(\"%c\", 10);\n"   

    meteraTraduccion(aux)   

# ------------------------------------------------------------------------- 
# OPERACIONES -------------------------------------------------------------
# ------------------------------------------------------------------------- 


def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):

    if isinstance(Exp, OPNum):
        return Exp.val
    elif isinstance(Exp, OPBinaria): 
        
        print('RESOLVIENDO BINARIA')
        print(Exp.term1, ' ', Exp.term2)
        if isinstance(Exp.term1, OPCadena) or isinstance(Exp.term2, OPCadena):
            x = resolverCadena(Exp, tablaSimbolos)
            print('retornando opcadena: ', x)
            return x

        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        if Exp.operador == ARITMETICA.MAS : 
            x = crearTemporal() + "=" + verificarT(exp1) + "+" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            return x
        if Exp.operador == ARITMETICA.MENOS :
            x = crearTemporal() + "=" + verificarT(exp1) + "-" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            return x
        if Exp.operador == ARITMETICA.ASTERISCO :
            x = crearTemporal() + "=" + verificarT(exp1) + "*" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            return x
        if Exp.operador == ARITMETICA.DIVIDIDO :
            x = crearTemporal() + "=" + verificarT(exp1) + "/" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            #hacer verificación de no /0
            return x
        if Exp.operador == ARITMETICA.MODULO :
            x = crearTemporal() + "=" + verificarT(exp1) + "%" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            #hacer verificación de no /0
            return x
        if Exp.operador == ARITMETICA.ELEVADO :
            x = crearTemporal() + "=" + verificarT(exp1) + "^" + verificarT(exp2) + ";"
            meteraTraduccion(x)
            return x
        else:  return None
    elif isinstance(Exp, OPNeg):
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == None:
            return None #esto lo dejo lo quito o lo cambio???

        x = crearTemporal() + "=0-" + verificarT(exp1) + ";"
        meteraTraduccion(x)
        return x
    
    #OPERACIONES NATIVAS NUMEROS
    elif isinstance(Exp, OPNativa):#log10, sin, cos, tan, sqrt
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == None:
            return None

        if Exp.tipo == MATH.LOG10 : return math.log10(exp1)
        if Exp.tipo == MATH.SIN : return math.sin(exp1)
        if Exp.tipo == MATH.COS : return math.cos(exp1)
        if Exp.tipo == MATH.TAN : return math.tan(exp1)
        if Exp.tipo == MATH.SQRT : return math.sqrt(exp1)
    elif isinstance(Exp, OPNativaLog):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        if exp1 == None or exp2 == None:
            return None

        return math.log(exp2, exp1)
    
    #OPERACIONES NATIVAS EXTRA
    elif isinstance(Exp, FParse):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos)

        if exp1 == None or exp2 == None:
            return None

        if exp1 == 'Float64':
            try:  
                return float(exp2)
            except:
                errordeTipos('Parse')
            return None
        elif exp1 == 'Int64':
            try:  
                return int(exp2)
            except:
                errordeTipos('Parse')
            return None
        else:
            errordeTipos('Parse')
            return None
    elif isinstance(Exp, FTrunc):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == None:
            return None

        try:  
            return math.trunc(float(exp1))
        except:
            errordeTipos('Trunc')
            return None      
    elif isinstance(Exp, FFloat):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == None:
            return None

        try:  
            return float(exp1)
        except:
            errordeTipos('Float')
            return None        
    elif isinstance(Exp, FString):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == None:
            return None

        return str(exp1)
 
    #OTROS
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:
            return x.valor
        else: 
            print('FALLA EN ID')
            return None
    elif isinstance(Exp, OPType):
        return getTipo(Exp)
    elif isinstance(Exp, OPNothing):
        return None
    elif isinstance(Exp, list):
        #print('Acá hay un arreglol')
        aux = []
        for term in Exp:
            if isinstance(term, OPNothing):
                return aux

            if isinstance(term, OPID):
                aux.append(term.id)
                continue
        
            x = resolverNumerica(term, tablaSimbolos)
            aux.append(x)
        return aux
    elif isinstance(Exp, LlamadaArr):
        arr_indices = []
        contadimensiones = 0
        for indice in Exp.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if tipoVariable(x) != 'Int64':
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(Exp.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        
        placeholder = ""
        try:
            if contadimensiones == 0: return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                placeholder = arr.valor[arr_indices[0]]
                return arr.valor[arr_indices[0]]
            elif contadimensiones == 2:
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]]
                return arr.valor[arr_indices[0]][arr_indices[1]]
            elif contadimensiones == 3: 
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
                return arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
        except Exception as e:
            print(e)
            return errorEquis('Asignación a arreglo', str(e))
    elif isinstance(Exp, FForRangoNum):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        if exp1 == None or exp2 == None:
            return None

        if tipoVariable(exp1) != 'Int64' and tipoVariable(exp2) != 'Int64':
            return None

        aux = []
        while exp1 <= exp2:
            aux.append(exp1)
            exp1 += 1

        return aux
    elif isinstance(Exp, LlamadaFuncion): 
        return None   
    else: 
        print('viendo si se va a las cadenas, ', Exp)
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverCadena(Exp, tablaSimbolos)


def resolverBooleana(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPLogica): 
        print('RESOLVIENDO LOGICA')
        print(Exp.term1, ' ', Exp.term2)

        exp1 = resolverBooleana(Exp.term1, tablaSimbolos)
        exp2 = resolverBooleana(Exp.term2, tablaSimbolos) 

        if Exp.operador == LOGICA.AND : return exp1 and exp2
        if Exp.operador == LOGICA.OR : return exp1 or exp2
        if Exp.operador == LOGICA.MAYORQUE : return exp1 > exp2
        if Exp.operador == LOGICA.MENORQUE : return exp1 < exp2
        if Exp.operador == LOGICA.MAYORIWAL : return exp1 >= exp2
        if Exp.operador == LOGICA.MENORIWAL : return exp1 <= exp2
        if Exp.operador == LOGICA.IWAL : return exp1 == exp2
        if Exp.operador == LOGICA.DISTINTO : return exp1 != exp2
        else:  return None
    elif isinstance(Exp, OPBool):
        if Exp.id == 'false':
            return False
        return True
    elif isinstance(Exp, OPNum):
        return Exp.val
    elif isinstance(Exp, OPCadena):
        return Exp.id
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:
            return x.valor
        else: 
            print('FALLA EN ID')
            return None
    elif isinstance(Exp, LlamadaArr):
        print("llamando arreglo")
        arr_indices = []
        contadimensiones = 0
        for indice in Exp.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if tipoVariable(x) != 'Int64':
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(Exp.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        
        try:
            if contadimensiones == 0: return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                return arr.valor[arr_indices[0]]
            elif contadimensiones == 2:
                return arr.valor[arr_indices[0]][arr_indices[1]]
            elif contadimensiones == 3: 
                return arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
        except Exception as e:
            print(e)
            return errorEquis('Asignación a arreglo', str(e))
    else: 
        print('viendo si se va a los numeros')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverNumerica(Exp, tablaSimbolos)


def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria):
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        #print(Exp.term2)
        #print(tipoVariable(exp2), ' ', exp2)

        if exp1 == None or exp2 == None:
            return None

        if Exp.operador == ARITMETICA.ASTERISCO : 
            return exp1 + str(exp2)
        if Exp.operador == ARITMETICA.ELEVADO and tipoVariable(exp2) == 'Int64' and exp2 != None: 
            
            copia = str(exp1)
            i = 1
            while i < exp2:
                copia += str(exp1)
                i += 1
            return copia
    elif isinstance(Exp, OPCadena):
        return Exp.id
    elif isinstance(Exp, OPLength):
        cad = resolverNumerica(Exp.term1, tablaSimbolos)
        if cad == None:
            return None
        
        return len(cad)
    elif isinstance(Exp, OPPop):
        nombre = ""
        
        if isinstance(Exp.arreglo, OPID):
            nombre = Exp.arreglo.id
            print('si hay nombre: ', nombre)

        arr = resolverNumerica(Exp.arreglo, tablaSimbolos)
        if arr == None:
            return None

        if tipoVariable(arr) != 'Array':
            errorEquis('Pop', 'el valor no es una lista')

        print('antes ->', arr)
        elemento = arr.pop()
        if nombre != "":
            print('despues ->', arr)
            obj = siExiste(nombre, tablaSimbolos)
            obj.valor = arr
            obj.nota = 'Actualización'
            tablaSimbolos.actualizar(obj)
            añadiraTabla(obj)
                
        return elemento
    elif isinstance(Exp, OPPush):
        nombre = ""
        if isinstance(Exp.arreglo, OPID):
            nombre = Exp.arreglo.id

        arr = resolverNumerica(Exp.arreglo, tablaSimbolos)
        if arr == None:
            return None

        if tipoVariable(arr) != 'Array':
            errorEquis('Push', 'el valor no es una lista')

        otro = resolverNumerica(Exp.term, tablaSimbolos)
        print('antes ->', arr)
        arr.append(otro)
        print('despues ->', arr)
        if nombre != "":
            obj = siExiste(nombre, tablaSimbolos)
            obj.valor = arr
            obj.nota = 'Actualización'
            tablaSimbolos.actualizar(obj)
            añadiraTabla(obj)
        return arr
    elif isinstance(Exp, OPLowercase):
        cad = resolverCadena(Exp.term1, tablaSimbolos)
        if cad == None:
            return None
        
        return str(cad).lower()
    elif isinstance(Exp, OPUppercase):
        cad = resolverCadena(Exp.term1, tablaSimbolos)
        if cad == None:
            return None
        
        return str(cad).upper()
    elif isinstance(Exp, OPMergeString):
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        print(Exp.term2)
        print(tipoVariable(exp2), ' ', exp2)

        if exp1 == None or exp2 == None:
            return None

        return exp1 + str(exp2)
    elif isinstance(Exp, OPElevarString):
        try: 
            exp1 = resolverCadena(Exp.term1, tablaSimbolos)
            if isinstance(Exp.term2, OPNum):
                exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
            else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

            print(Exp.term2)
            print(tipoVariable(exp2), ' ', exp2)

            if exp1 == None or exp2 == None:
                return None
            if tipoVariable(exp2) == 'Int64' and exp2 != None: 
            
                copia = str(exp1)
                i = 1
                while i < exp2:
                    copia += str(exp1)
                    i += 1
                return copia        
        except: return None
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:

            return x.valor
        else: 
            print('FALLA EN ID')
            return None
    elif isinstance(Exp, LlamadaArr):
        arr_indices = []
        contadimensiones = 0
        for indice in Exp.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if tipoVariable(x) != 'Int64':
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(Exp.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        
        placeholder = ""
        try:
            if contadimensiones == 0: return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                placeholder = arr.valor[arr_indices[0]]
                return arr.valor[arr_indices[0]]
            elif contadimensiones == 2:
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]]
                return arr.valor[arr_indices[0]][arr_indices[1]]
            elif contadimensiones == 3: 
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
                return arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
        except Exception as e:
            print(e)
            return errorEquis('Asignación a arreglo', str(e))
    else:
        print('viendo si se va a las lógicas')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverBooleana(Exp, tablaSimbolos)


# ------------------------------------------------------------------------- 
# AUXILIARES --------------------------------------------------------------
# ------------------------------------------------------------------------- 

def siExiste(nombre, tablaSimbolos: cst.TablaSimbolos):
    aux = tablaSimbolos.obtener(nombre)
    if isinstance(aux, cst.NodoErrorSemantico):
        return False
    else: return aux

def siExisteHardcore(nombre, tablaSimbolos: cst.TablaSimbolos):
    aux = tablaSimbolos.obtener(nombre)
    if isinstance(aux, cst.NodoErrorSemantico):
        desc = "Error semántico - no se encuentra la variable: " + str(nombre)
        global contaerrores
        nuevo = cst.NodoErrorSemantico(desc)
        nuevo.contador = contaerrores
        contaerrores += 1
        global listasemanticos
        listasemanticos.append(nuevo)
        return False
    else: return aux

def añadiraTabla(simbolo: cst.NodoSimbolo):
    global lista_simbolos
    lista_simbolos.append(simbolo)

def getTipo(tipo: OPType):
    if isinstance(tipo.id, OPID):
        return tipo.id.id
    else :
        return tipo.id
    
def tipoVariable(var):
    x = str(type(var))
    if 'str' in x:
        return 'String'
    elif 'list' in x:
        return 'Array'
    elif 'int' in x:
        return 'Int64'
    elif 'float' in x:
        return 'Float64'
    elif 'dict' in x:
        return 'Struct'
    elif 'bool' in x:
        return 'Bool'
    elif 'None' in x:
        return 'None'

def errordeTipos(nombre_instruccion):
    desc = "Error semántico con la instruccion: "+ nombre_instruccion +". Los tipos no son compatibles"
    global contaerrores
    nuevo = cst.NodoErrorSemantico(desc)
    nuevo.contador = contaerrores
    contaerrores += 1
    global listasemanticos
    listasemanticos.append(nuevo)

def errorEquis(nombre_instruccion, razon):
    desc = "Error semántico con la instruccion: "+ nombre_instruccion +". "+ razon
    global contaerrores
    nuevo = cst.NodoErrorSemantico(desc)
    nuevo.contador = contaerrores
    contaerrores += 1
    global listasemanticos
    listasemanticos.append(nuevo)
    return None


# ------------------------------------------------------------------------- 
# COMPILADOR --------------------------------------------------------------
# ------------------------------------------------------------------------- 

def verificarT(expr):
    txt = str(expr)
    if "=" in txt:
        nombre = txt.split("=")
        return nombre[0]
    return txt

def crearTemporal():
    global contatemporales
    x = contatemporales
    contatemporales += 1
    return "t" + str(x)

def meteraTraduccion(texto):
    global traducciontemporal
    traducciontemporal += texto
    traducciontemporal += '\n'

def meterPalabra(texto):
    for i in texto:
        ascii = ord(i)
        aux = "fmt.Printf(\"%c\"," +  +");\n"
        meteraTraduccion(aux)
