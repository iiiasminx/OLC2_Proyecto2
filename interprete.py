# importo todo de todos lados
from sys import exc_info
from a_lexico import fighting, tokens
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 
import math

lista_simbolos = [] # acá van todos los valores que se hayan declarado
arbol =[]
ts_global = cst.TablaSimbolos()
contaerrores = 0
listasemanticos = []
textoimpresion = ""
contabucle = 0
pilaentornos = []
extra = ""


def fightingfinal(texto):
    global textoimpresion
    textoimpresion = """Learn Python
    Programming"""


    exportef = fighting2(texto)
    global arbol 
    arbol = exportef.arbol
    global lista_simbolos
    lista_simbolos = []
    global listasemanticos
    listasemanticos = []
    global contaerrores
    contaerrores = 0
    
    global ts_global
    ts_global.simbolos.clear()
    pilaentornos.clear()
    pilaentornos.append('global')

    
    procesarInstrucciones(arbol, ts_global)

    #print(ts_global.simbolos)
    exportef.interpretacion = textoimpresion
    exportef.tabla_simbolos = lista_simbolos
    exportef.listasemanticos = listasemanticos
    listasegundos = ts_global.simbolos.values()
    exportef.listasegundos = listasegundos

    return exportef

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

        if extra != "" : return
        if isinstance(instruccion, Impresion): intImpresion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Impresionln): intImpresionLN(instruccion, tablaSimbolos)


        elif isinstance(instruccion, Declaracion): intDeclaracion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Scope): intScope(instruccion, tablaSimbolos)


        elif isinstance(instruccion, DefFuncion): intDefFuncion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, DefFuncParam): intDefFuncParam(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FuncParams): intDefFuncParam(instruccion, tablaSimbolos)

        elif isinstance(instruccion, LlamadaFuncion): intLlamadaFuncion(instruccion, tablaSimbolos)

        elif isinstance(instruccion, FIFuni): intFIFuni(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FIF): intFIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FElseIF): intFElseIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FELSE): intFELSE(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FWhile): intFWhile(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FFor): intFFor(instruccion, tablaSimbolos)

        elif isinstance(instruccion, SBreak): 
            print('BREAK DETECTADP')
            extra =  OPTransferencia(1)
            break
        elif isinstance(instruccion, SContinue): 
            print('CONTINUE DETECTADP')
            extra =  OPTransferencia(2)
            break
        elif isinstance(instruccion, SReturn): 
            print('Return DETECTADP')
            extra =  OPTransferencia(3, instruccion.contenido)
            break
        elif isinstance(instruccion, DeclStruct): intDeclStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, ConstruccionStruct): intConstruccionStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, AsignacionAtributosStruct): intAsignacionAtributosStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, AccesoAtributo): intAccesoAtributo(instruccion, tablaSimbolos)        
        elif isinstance(instruccion, OPPASS): print('-')
        elif isinstance(instruccion, OPPop):
            nombre = ""
            
            if isinstance(instruccion.arreglo, OPID):
                nombre = instruccion.arreglo.id
                print('si hay nombre: ', nombre)

            arr = resolverNumerica(instruccion.arreglo, tablaSimbolos)
            if arr == None:
                continue

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
                    
            continue
        elif isinstance(instruccion, OPPush):
            nombre = ""
            if isinstance(instruccion.arreglo, OPID):
                nombre = instruccion.arreglo.id

            arr = resolverNumerica(instruccion.arreglo, tablaSimbolos)
            if arr == None:
                continue

            if tipoVariable(arr) != 'Array':
                errorEquis('Push', 'el valor no es una lista')

            otro = resolverNumerica(instruccion.term, tablaSimbolos)
            print('antes ->', arr)
            arr.append(otro)
            print('despues ->', arr)
            if nombre != "":
                obj = siExiste(nombre, tablaSimbolos)
                obj.valor = arr
                obj.nota = 'Actualización'
                tablaSimbolos.actualizar(obj)
                añadiraTabla(obj)
            continue
    
        else :
            desc = "Error semántico con la instruccion número: " + str(contador) + " de " + str(pilaentornos[-1])
            global contaerrores
            nuevo = cst.NodoErrorSemantico(desc)
            nuevo.contador = contaerrores
            contaerrores += 1
            global listasemanticos
            listasemanticos.append(nuevo)

        
        print('\n', instruccion)

# ------------------------------------------------------------------------- 
# Inicio Auxiliares -------------------------------------------------------
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
# Inicio Operaciones ------------------------------------------------------
# ------------------------------------------------------------------------- 

def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria):
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        print(Exp.term2)
        print(tipoVariable(exp2), ' ', exp2)

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


# numericas
def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria): 
        
        print('RESOLVIENDO BINARIA')
        print(Exp.term1, ' ', Exp.term2)
        if isinstance(Exp.term1, OPCadena) or isinstance(Exp.term2, OPCadena):
            x = resolverCadena(Exp, tablaSimbolos)
            print('retornando opcadena: ', x)
            return x

       # if not isinstance(Exp.term1, OPNum) and not isinstance(Exp.term2, OPNum): 
       #     if not isinstance(Exp.term1, OPBinaria) and not isinstance(Exp.term2, OPBinaria):
       #         print('metiendome al if2')
       #         return resolverCadena(Exp, tablaSimbolos)

        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        if exp1 == None or exp2 == None:
            return None

        if tipoVariable(exp1) != 'Int64' and tipoVariable(exp2) != 'Int64':
            if tipoVariable(exp1) != 'Float64' and tipoVariable(exp2) != 'Float64':
                print('metiendome al if3')
                return resolverCadena(Exp, tablaSimbolos)

        if Exp.operador == ARITMETICA.MAS : return exp1 + exp2
        if Exp.operador == ARITMETICA.MENOS : return exp1 - exp2
        if Exp.operador == ARITMETICA.ASTERISCO : return exp1 * exp2
        if Exp.operador == ARITMETICA.DIVIDIDO : return exp1 / exp2
        if Exp.operador == ARITMETICA.MODULO : return exp1 % exp2
        if Exp.operador == ARITMETICA.ELEVADO : return exp1 ** exp2
        else:  return None
    elif isinstance(Exp, OPNeg):
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == None:
            return None

        return - exp1
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
    elif isinstance(Exp, Ftypeof):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)

        return tipoVariable(exp1)
    elif isinstance(Exp, OPNum):
        return Exp.val
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
        return intLlamadaFuncion(Exp, tablaSimbolos)    
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

        print(exp1, ' ', exp2)
        if exp1 == 'Failed' or exp2 == 'Failed':
            return None
        
        if exp1 == None or exp2 == None:
            return None

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


# ------------------------------------------------------------------------- 
# Inicio Interprete -------------------------------------------------------
# ------------------------------------------------------------------------- 

# Impresion ---------------------------------------------------------------
# -------------------------------------------------------------------------
def intImpresion(instr, tablaSimbolos: cst.TablaSimbolos):
    print('impresion')
    aux = ""

    for instruccion in instr.texto:
        aux += str(resolverNumerica(instruccion, tablaSimbolos))

    global textoimpresion
    textoimpresion += aux

def intImpresionLN(instr, tablaSimbolos : cst.TablaSimbolos):
    print('impresionLN')
    aux = ""

    for instruccion in instr.texto:
        aux += str(resolverNumerica(instruccion, tablaSimbolos))

    aux += "\n"
    global textoimpresion
    textoimpresion += aux

#variables ----------------------------------------------------------------
# -------------------------------------------------------------------------
def intDeclaracion(instr:Asignacion, tablaSimbolos : cst.TablaSimbolos): #ver si necesito más de estas
    print('intDeclaracion')
    print(instr.valor)

    valor = resolverNumerica(instr.valor, tablaSimbolos)
    aux = siExiste(instr.nombre[0].id, tablaSimbolos)
    tipo = tipoVariable(valor)
    ambito = pilaentornos[-1]

    if aux:
        print('actualizando')
        if aux.tipo == 'Function':
            errorEquis('Asignación', 'ya existe una funcion con este nombre')
            return None
        # actualizo el valor
        simbolo = cst.NodoSimbolo(instr.nombre[0].id, tipo, ambito, valor)
        simbolo.nota = 'Actualización'
        tablaSimbolos.actualizar(simbolo)
        añadiraTabla(simbolo)
        return True
    else:
        print('nuevo')
        # creo una nueva variable
        simbolo = cst.NodoSimbolo(instr.nombre[0].id, tipo, ambito, valor)
        tablaSimbolos.agregar(simbolo)
        añadiraTabla(simbolo)
        return True

def intScope(instr: Scope, tablaSimbolos : cst.TablaSimbolos): #ver si cambio este por otro como lo hice en el sintactico
    print('Asignando')

    global pilaentornos
    ambito = pilaentornos[-1]
    if instr.scope == 'global':
        ambito = instr.scope

    try: 
    #si lo que está a la izq es un array 
        if isinstance(instr.asignacion.nombre, LlamadaArr):
            print('ESUNARRAY')
            print(instr.asignacion.nombre.nombre, ' , ', instr.asignacion.nombre.inds)
            valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)

            arr_indices = []
            contadimensiones = 0
            for indice in instr.asignacion.nombre.inds:
                x = resolverNumerica(indice, tablaSimbolos)
                print (tipoVariable(x), ' , ', x)

                if tipoVariable(x) != 'Int64':
                    errordeTipos('Asignacion de Array')
                    return None

                arr_indices.append(x)
                contadimensiones += 1

            arr = siExisteHardcore(instr.asignacion.nombre.nombre, tablaSimbolos)
            if arr == False or not arr:
                return None
            
            placeholder = ""
            try:
                if contadimensiones == 0: return errordeTipos('Asignación a arreglo')
                elif contadimensiones == 1: 
                    placeholder = arr.valor[arr_indices[0]]
                    arr.valor[arr_indices[0]] = valor
                elif contadimensiones == 2:
                    placeholder = arr.valor[arr_indices[0]][arr_indices[1]]
                    arr.valor[arr_indices[0]][arr_indices[1]] = valor
                elif contadimensiones == 3: 
                    placeholder = arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
                    arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]] = valor
            except Exception as e:
                print(e)
                return errorEquis('Asignación a arreglo', str(e))

            print('valor de arr izq: ', placeholder)
            if placeholder == "":
                return
            arr.nota = 'Actualización Array'
            tablaSimbolos.actualizar(arr)
            añadiraTabla(arr)

        # si lo que esta a la izq del parentesis es un id
        elif isinstance(instr.asignacion.nombre[0], OPID):
            
            print('VAL ->',instr.asignacion.valor)
            valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)
            aux = siExiste(instr.asignacion.nombre[0].id, tablaSimbolos)
            if isinstance(instr.asignacion, Asignacion) : 
                tipo = tipoVariable(valor)
                if aux:
                    print('actualizando')
                    if aux.tipo == 'Function':
                        errorEquis('Asignación', 'ya existe una funcion con este nombre')
                        return
                    # actualizo el valor
                    simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, tipo, ambito, valor)
                    simbolo.nota = 'Actualización'
                    tablaSimbolos.actualizar(simbolo)
                    añadiraTabla(simbolo)
                else:
                    print('nuevo')
                    # creo una nueva variable
                    simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, tipo, ambito, valor)
                    tablaSimbolos.agregar(simbolo)
                    añadiraTabla(simbolo)
            elif isinstance(instr.asignacion, AsignacionTipada): 
                if aux:
                    print('actualizando')
                    # actualizo el valor
                    simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, getTipo(instr.asignacion.tipo), ambito, valor)
                    simbolo.nota = 'Actualización'
                    tablaSimbolos.actualizar(simbolo)
                    añadiraTabla(simbolo)
                else:
                    print('nuevo')
                    # creo una nueva variable
                    simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, getTipo(instr.asignacion.tipo), ambito, valor)
                    tablaSimbolos.agregar(simbolo)
                    añadiraTabla(simbolo)
    except Exception as ee:
        errorEquis('Asignación', 'algo x pasó :c')

# Funciones ---------------------------------------------------------------
# -------------------------------------------------------------------------
def intDefFuncion(instr: DefFuncion, tablaSimbolos : cst.TablaSimbolos):
    print('DefFunction')
    print('nombre = ', instr.nombre)
    #print('params = ', instr.params)
    print('instrucciones = ', instr.instrucciones)

    #geteando un array con parámetros -- nombre y tipo en string
    params = []
    solonombres = []
    for parametro in instr.params:
        x = intDefFuncParam(parametro, tablaSimbolos)
        params.append(x)
        solonombres.append(x.id)
        print( x.id, ' , ', x.tipo)
    
    # si ya existe una variable con este nombre, x
    aux = siExiste(instr.nombre, tablaSimbolos)
    if aux:
        print('ya existe')
        errorEquis('DefFunc', 'ya existe una función con ese nombre :C')
        return
    else:
        print('nuevo')
        # creo una nueva variable
        simbolo = cst.NodoSimbolo(instr.nombre, 'Function', str(solonombres), '-')
        simbolo.funcinstrucciones = instr.instrucciones #listadeinstrucciones
        simbolo.funcparams = params
        tablaSimbolos.agregar(simbolo)
        añadiraTabla(simbolo)

def intDefFuncParam(instr: DefFuncParam, tablaSimbolos : cst.TablaSimbolos):
    tipo = ""
    if instr.tipo != "":
        tipo = getTipo(instr.tipo)

    return (ParamF(instr.param.id, tipo))
def intLlamadaFuncion(instr: LlamadaFuncion, tablaSimbolos : cst.TablaSimbolos):
    print('LlamadaFunc')
    print('nombre: ', instr.funcion)
    print('params enviados: ', instr.params)
    global pilaentornos
    pilaentornos.append('funcion')

    #verificando si la función existe (y es funcion)
    aux = siExiste(instr.funcion, tablaSimbolos)
    if aux:
        if aux.tipo != 'Function':
            print(aux.tipo, ' no es Function')
            errordeTipos('Llamada a función')
            return

        #verificando los parámetros
        if len(instr.params) != len(aux.funcparams):
            print(len(instr.params), ' no es ', len(aux.ambito))
            errorEquis('Llamada funcion', 'Los parámetros no son los correctos')
            return
        
        contador = 0
        #funcparams = nombre, tipo
        #param = cosox
        for param in instr.params:
            if aux.funcparams[contador].tipo == '':
                contador += 1
                continue
            
            valorparam = resolverNumerica(param, tablaSimbolos)
            if aux.funcparams[contador].tipo != tipoVariable(valorparam):
                print('params no compatibles')
                errordeTipos('LLamada Funcion - Params')
                return           
            
            contador+= 1

        print ('TEST PASADO :D')

        #ya puedo empezar a ver que pez
        instruccionesfuncion = aux.funcinstrucciones
        global ts_global
        ts_local = ts_global
        global extra

        contador = 0
        for param in instr.params:
            intDeclaracion(Asignacion([aux.funcparams[contador]], param), ts_local)
            contador += 1   

        procesarInstrucciones(instruccionesfuncion, ts_local)   
        
        #si es un arreglo lo paso por referencia

        if extra != "":
           print('SENTENCIA RECIBIDAFN')
           if extra.tipo == 1: 
               errorEquis('funcion', 'break outsode loop')
               pilaentornos.pop()
               extra = ""
               return None
           if extra.tipo == 2: 
               errorEquis('funcion', 'continue outsode loop')
               pilaentornos.pop()
               extra = ""
               return None
           if extra.tipo == 3: 
               pilaentornos.pop()
               ret = extra.obj
               print('EL RETORNO ES: ', ret)
               ret = resolverNumerica(extra.obj, ts_local)
               extra = ""
               return ret
          
    else:
        errorEquis('LLamada a función', 'la función no existe') 
        return
    


# Condicionales -----------------------------------------------------------
# -------------------------------------------------------------------------

def intFIFuni(instr, tablaSimbolos : cst.TablaSimbolos):
    print('if')

    global pilaentornos
    pilaentornos.append('if')
    print('oplog', instr.oplog)
    print('instruccionesv : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global

    if resolverBooleana(instr.oplog, tablaSimbolos):       
        procesarInstrucciones(instr.instruccionesv, ts_local)
        if extra != "":
           print('SENTENCIA RECIBIDAIF')
           return
    else:
        procesarInstrucciones([instr.instruccionesf], ts_local)
        if extra != "":
           print('SENTENCIA RECIBIDAIF')
           return

    pilaentornos.pop()
def intFIF(instr, tablaSimbolos : cst.TablaSimbolos):
    print('if')

    global pilaentornos
    pilaentornos.append('if')
    print('oplog', instr.oplog)
    print('instruccionesv : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global

    if resolverBooleana(instr.oplog, tablaSimbolos):       
        procesarInstrucciones(instr.instruccionesv, ts_local)
        if extra != "":
           print('SENTENCIA RECIBIDAIF')
           return
    else:
        procesarInstrucciones([instr.instruccionesf], ts_local)
        if extra != "":
           print('SENTENCIA RECIBIDAIF')
           return

    pilaentornos.pop()
def intFElseIF(instr, tablaSimbolos : cst.TablaSimbolos):
    print('elif')

    global pilaentornos
    pilaentornos.append('elif')
    print('oplog', instr.oplog)
    print('instrucciones : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global

    if resolverBooleana(instr.oplog, tablaSimbolos):       
        procesarInstrucciones(instr.instruccionesv, ts_local)
    else:
        procesarInstrucciones([instr.instruccionesf], ts_local)


    pilaentornos.pop()
def intFELSE(instr, tablaSimbolos : cst.TablaSimbolos):
    print('else')

    global pilaentornos
    pilaentornos.append('else')
    global ts_global
    ts_local = ts_global

    procesarInstrucciones(instr.instrucciones, ts_local)

    pilaentornos.pop()
def intFWhile(instr : FWhile, tablaSimbolos : cst.TablaSimbolos):
    print('while')

    global pilaentornos
    pilaentornos.append('while')
    print('oplog', instr.oplog)
    print('instrucciones : ', instr.instrucciones)

    global ts_global
    ts_local = ts_global

    reotrnable =  ""
    while resolverBooleana(instr.oplog, tablaSimbolos):  

       procesarInstrucciones(instr.instrucciones, ts_local)  
       global extra
       if extra != "":
           print('SENTENCIA RECIBIDAWH')
           if extra.tipo == 1: break
           if extra.tipo == 2: continue
           if extra.tipo == 3: 
               reotrnable = extra.obj
               break    

    pilaentornos.pop()
    return reotrnable
def intFFor(instr: FFor, tablaSimbolos : cst.TablaSimbolos):

    print('for')

    global pilaentornos
    pilaentornos.append('for')

    print('Instrucciones', instr.instrucciones)
    print('id =', instr.var)
    rangoraw = resolverNumerica(instr.rango, tablaSimbolos)
    print('rangoraw ', rangoraw)

    if tipoVariable(rangoraw) != 'String' and tipoVariable(rangoraw) != 'Array':
        errordeTipos('Rango de For')
        return None

    global ts_global
    ts_aux = ts_global
    reotrnable = ""
    global extra
    
    
    #si el rango es una cadena 
    if tipoVariable(rangoraw) == 'String':
        x = intDeclaracion(Asignacion([OPID(instr.var)], OPCadena(rangoraw[0])), ts_aux)
        if x == None:
            return 
        
        for i in rangoraw:
            y = intDeclaracion(Asignacion([OPID(instr.var)], OPCadena(i)), ts_aux)
            if y == None:
                return 

            procesarInstrucciones(instr.instrucciones, ts_aux)              
            if extra != "":
                print('SENTENCIA RECIBIDA')
                if extra.tipo == 1: break
                if extra.tipo == 2: continue
                if extra.tipo == 3: 
                    reotrnable = extra.obj
                    break 
    # si e rango es un arreglo
    else:
        x = intDeclaracion(Asignacion([OPID(instr.var)], OPNum(rangoraw[0])), ts_aux)
        if x == None:
            return 
        
        for i in rangoraw: 
            y =  intDeclaracion(Asignacion([OPID(instr.var)], OPCadena(i)), ts_aux)
            if y == None:
                return 
            procesarInstrucciones(instr.instrucciones, ts_aux)
            if extra != "":
                print('SENTENCIA RECIBIDA')
                if extra.tipo == 1: break
                if extra.tipo == 2: continue
                if extra.tipo == 3: 
                    reotrnable = extra.obj
                    break

# Struct ------------------------------------------------------------------
# -------------------------------------------------------------------------
def intDeclStruct(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

def intConstruccionStruct(instr, tablaSimbolos : cst.TablaSimbolos):# esto es en p = Carro(1,2)
    pass

def intAsignacionAtributosStruct(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

def intAccesoAtributo(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

