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
pilaentornos = []

contabucle = 0
extra = ""

contatemporales = 0
contasaltos = 0
contaposiciones = 0
p = 0
h = 0

traduccion = ""
traducciontemporal = ""
tradfunciones = ""

# strings para la traduccion
siwal = " = "
fincomando = ";\n"
smas = " + "
smenos = " - "

#funciones extra
yapotencia = False

def compilando(texto):
    # seteando todo como debe ser :v
    global contatemporales
    contatemporales = 0
    global contaposiciones
    contaposiciones = 0
    global contasaltos
    contasaltos = 0
    global lista_simbolos
    lista_simbolos = []
    global ts_global
    ts_global.simbolos.clear()
    pilaentornos.clear()
    pilaentornos.append('global')
    global listasemanticos
    listasemanticos = []
    funcionesencero()

    global traduccion 
    global traducciontemporal
    traducciontemporal = ""  
    global tradfunciones
    tradfunciones = ""

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

    if contatemporales > 0: 
        traduccion += "var "

        for i in range(contatemporales):
            if i == contatemporales-1:
                traduccion +=  "t" + str(i) + " float64\n\n"
            else:
                traduccion +=  "t" + str(i) + ", "

    
    traduccion += "//------FUNCIONES------\n"
    traduccion += tradfunciones

    traduccion += "\n//--------MAIN--------\n"
    traduccion += "func main() {\n"
    traduccion += "P = 0; H = 0;\n\n"
    traduccion += traducciontemporal
    traduccion += "}"  

    paquete.traduccion = traduccion  
    paquete.errores_lexicos =lexicos
    paquete.tabla_simbolos = lista_simbolos
    paquete.listasemanticos = listasemanticos

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

        elif isinstance(instruccion, Declaracion): intDeclaracion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Scope): intScope(instruccion, tablaSimbolos)


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
# DECLARACION -------------------------------------------------------------
# -------------------------------------------------------------------------

def intDeclaracion(instr:Asignacion, tablaSimbolos : cst.TablaSimbolos):
    return ""

def intScope(instr: Scope, tablaSimbolos : cst.TablaSimbolos):
    print('Asignando en scope')

    ambito = 'local'
    if instr.scope == 'global':
        ambito = 'global'

    asignacion = instr.asignacion
    valor = resolverNumerica(asignacion.valor, tablaSimbolos)
    aux = siExiste(asignacion.nombre[0].id, tablaSimbolos)
    tipo = tipoVariable(valor)
    if asignacion.tipo != "":
        tipo = asignacion.tipo.id
        if tipo != tipoVariable(valor):
            errordeTipos("Declaración de " + asignacion.nombre[0].id)

    if aux:
        print('actualizando')
    else:
        print('nuevo')
        # creo una nueva variable
        posicion = crearposicion()

        simbolo = cst.NodoSimbolo(asignacion.nombre[0].id, tipo, ambito, posicion)
        tablaSimbolos.agregar(simbolo)
        añadiraTabla(simbolo)

        #acá meto mi c3d

        x = ""
        if tipo == "Int64" or tipo == "Float64":
            x += getStack(posicion) + siwal + str(valor) + fincomando        
        elif tipo == "Bool":
            print('-->', valor)
            if valor == "False" or valor == "false" or valor == False:
                valor = 0
            else:
                valor = 1
            x += getStack(posicion) + siwal + str(valor) + fincomando  
        elif tipo == "String":
            x += ""      

        meteraTraduccion(x)
        return ""

    

# ------------------------------------------------------------------------- 
# OPERACIONES -------------------------------------------------------------
# ------------------------------------------------------------------------- 


def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    global smas
    global smenos
    global fincomando
    global siwal

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
            resultado = crearTemporal()
            noerror = crearSalto()
            restocodigo = crearSalto()
            
            x = crearIf(verificarT(exp2) + " != 0", noerror)
            x += meterPalabra("MathError")
            x += resultado + siwal + "0" + fincomando
            x += iniciarGoto(restocodigo)
            x += iniciarSalto(noerror)
            x += resultado + "=" + verificarT(exp1) + "/" + verificarT(exp2) + fincomando
            x += iniciarSalto(restocodigo)
            meteraTraduccion(x)

            return resultado
        if Exp.operador == ARITMETICA.MODULO :
            resultado = crearTemporal()
            noerror = crearSalto()
            restocodigo = crearSalto()
            
            x = crearIf(verificarT(exp2) + " != 0", noerror)
            x += meterPalabra("MathError")
            x += resultado + siwal + "0" + fincomando
            x += iniciarGoto(restocodigo)
            x += iniciarSalto(noerror)
            x += resultado + "= float64( int64(" + verificarT(exp1) + ") % int64(" + verificarT(exp2) + "))" + fincomando
            x += iniciarSalto(restocodigo)
            meteraTraduccion(x)

            return resultado
        if Exp.operador == ARITMETICA.ELEVADO :

            # HACIENDO LA FUNCION DE ELEVADO
            global yapotencia
            if not yapotencia: 
                temp1 = crearTemporal() #temporal del ambito
                tempstack = crearTemporal() #este es numero al que se eleva
                copia1 = crearTemporal() # este es el # que se está elevando
                copia2 = crearTemporal()
                x = temp1 + " = " + getP("+1") 
                x += tempstack + " = " + getStack(temp1) + ";\n"
                x += copia1 + " = " + tempstack + ";\n"
                x += copia2 + " = " + tempstack + ";\n"
                x += temp1 + " = " + getP("+2")
                x += tempstack + " = " + getStack(temp1) + ";\n"

                comparacion = tempstack + " == 0"
                saltofinal = crearSalto()   # si es 0
                saltopenultimo = crearSalto() #si es 1
                saltox = crearSalto() #si es cualquier otro
                saltoreturn = crearSalto()

                x += crearIf(comparacion, saltofinal) # si ya es el final de las iteraciones
                x += iniciarSalto(saltox)
                x += crearIf(tempstack + " <= 1", saltopenultimo)
                # si no es ni 0 ni uno, comienzo a multiplicar
                x += copia1 + " = " + copia1 + "*" + copia2 + ";\n"
                x += tempstack  + " = " + tempstack + "- 1"  + ";\n"
                x += iniciarGoto(saltox)

                x += iniciarSalto(saltopenultimo)
                x += getStack("P") + " = " + copia1 + ";\n"
                x += iniciarGoto(saltoreturn)

                x += iniciarSalto(saltofinal) # si está elevado a la 0, fijo fijo va a ser 1
                x += getStack("P") + "= 1;\n"
                x += iniciarSalto(saltoreturn)
                x += "return;"

                meterfuncion("potencia", x)
                yapotencia = True

            # HACIENDO LO QUE VA EN EL MAIN
            
            posicionStack = crearTemporal()
            respuesta = crearTemporal()
            y = ""
            aux = ""
            aux2 = ""
            #si alguna de las exps es un temporal, p sube uno
            if "t" in verificarT(exp1) or "t" in verificarT(exp2):
                aux =  " = " + getP("+1")
                aux2 =  " = " + getP("-1")
            else:
                aux =  " = " + getP("+0")
                aux2 =  " = " + getP("-0")
            
            y += posicionStack + aux
            y += posicionStack + " = " + posicionStack + "+1;\n" #en una nueva posicion de stack
            y += getStack(posicionStack) + siwal + verificarT(exp1) + fincomando
            y += tempmasmas(posicionStack)
            y += getStack(posicionStack) + siwal + verificarT(exp2) + fincomando

            y += "P" + aux
            y += "potencia()" + fincomando
            y += respuesta + siwal + getStack("P") + fincomando
            y += "P" + aux2  

            meteraTraduccion(y)

            return respuesta
        else:  return ""
    elif isinstance(Exp, OPNeg):
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == None:
            return "" 

        x = crearTemporal() + "=0-" + verificarT(exp1) + fincomando
        meteraTraduccion(x)
        return x
    
    #OPERACIONES NATIVAS NUMEROS
    elif isinstance(Exp, OPNativa):
        return ""
    elif isinstance(Exp, OPNativaLog):
        return ""
    
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
            return ""
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

def funcionesencero():
    global yapotencia
    yapotencia = False

def meterPalabra(texto):
    aux = ""
    for i in texto:
        ascii = ord(i)
        aux += "fmt.Printf(\"%c\"," + str(ascii) +");\n"
    return aux

# TABLA DE SIMBOLOS
def crearposicion():
    global contaposiciones
    x = contaposiciones
    contaposiciones += 1
    return x

# TRADUCCION
def meteraTraduccion(texto):
    global traducciontemporal
    traducciontemporal += texto
    traducciontemporal += '\n'

def meterfuncion(nombre: str,texto:str):
    global tradfunciones
    tradfunciones += "func " + nombre + "() {\n"
    tradfunciones += texto
    tradfunciones += "\n}\n"

# IF
def crearIf(comparacion, goto):
    x = "if(" + comparacion + ") {goto " + goto + "}\n"
    return x


# SALTOS
def crearSalto():
    global contasaltos
    x = contasaltos
    contasaltos += 1
    return "L" + str(x)

def getSalto(indice): 
    global contasaltos
    x = contasaltos - indice -1
    return "L" + str(x)

def iniciarSalto(salto):
    return salto + ":\n"

def iniciarGoto(salto):
    return "goto " + salto + ";\n"

# TEMPORALES
def crearTemporal():
    global contatemporales
    x = contatemporales
    contatemporales += 1
    return "t" + str(x)

def getTemporal(indice): 
    global contatemporales
    x = contatemporales - indice -1
    return "t" + str(x)

def verificarT(expr):
    txt = str(expr)
    if "=" in txt:
        nombre = txt.split("=")
        return nombre[0]
    return txt

def tempmasmas(temp):
    return temp + " = " + temp + "+1;\n"

def tempmenosmenos(temp):
    return temp + " = " + temp + "-1;\n"    

# P 
def aumentarP(unidades):
    global p
    p = p + unidades
    trad = "P=P+" + str(unidades) + ";"
    meteraTraduccion(trad)

def disminuirP(unidades):
    global p
    p = p - unidades
    trad = "P=P-" + str(unidades) + ";"
    meteraTraduccion(trad)

def getP(mod):
    return "P" + mod + ";\n"

# H
def aumentarH(unidades):
    global h
    h = h + unidades
    trad = "H=H+" + str(unidades) + ";"
    meteraTraduccion(trad)

def disminuirH(unidades):
    global h
    h = h - unidades
    trad = "H=H-" + str(unidades) + ";"
    meteraTraduccion(trad)

def getH(mod):
    return "H" + mod + ";\n"

# HEAP
def getHeap(temporal):
    return "heap[" + str(temporal) + "]"

# STACK
def getStack(temporal):
    return "stack[int(" + str(temporal) + ")]"