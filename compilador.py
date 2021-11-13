# importo todo de todos lados
from sys import exc_info, getsizeof
from a_lexico import fighting, tokens
from interprete import intAsignacionAtributosStruct
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

#funcionusada 0 binaria, 1 strings, 2 bools, 3 nothing, 4 array, 5 llamadaArr
funcionusada = 0

#funciones extra
yapotencia = False
yaconcatstring = False
yaprintstring = False
yacomparestrings = False
yalowercase = False
yauppercase = False
yagenerarArray = False

# vars extra
usandovars = 0 # las vars de la instruccion
contavars = 0   #las vars del todo
saltotrue = ""
saltofalse = ""
saltorest = ""
ultimorest = ""

usandologica = [2] # pila de cosos
comparandocadenas = False
gotos = []
inicioloop = ""
findeloop = ""
varglobal = ""

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
    global ultimorest
    ultimorest = crearSalto()

    traduccion = """package main\nimport ("fmt")\n"""
    traduccion += "var stack [300000]float64\nvar heap [300000]float64\n"
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

    else:
        traduccion += "var t0 float64\n\n"

    
    traduccion += "//------FUNCIONES------\n"
    traduccion += tradfunciones

    traduccion += "\n//--------MAIN--------\n"
    traduccion += "func main() {\n"
    traduccion += "P = 0; H = 0;\n\n"
    traduccion += traducciontemporal
    traduccion += iniciarGoto(ultimorest)
    traduccion += iniciarSalto(ultimorest)
    traduccion += "}"  

    trad = checarLabelsNoUsadas(traduccion)

    paquete.traduccion = trad  
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
        instruccionesencero()

        #OPERACIONES
        if extra != "" : return
        if isinstance(instruccion, Impresion): intImpresion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Impresionln): intImpresionLN(instruccion, tablaSimbolos)

        elif isinstance(instruccion, Declaracion): intDeclaracion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Scope): intScope(instruccion, tablaSimbolos)

        elif isinstance(instruccion, FIFuni): intFIFuni(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FIF): intFIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FElseIF): intFElseIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FELSE): intFELSE(instruccion, tablaSimbolos)

        elif isinstance(instruccion, FWhile): intFWhile(instruccion, tablaSimbolos)
        elif isinstance(instruccion, SBreak): intBreak(instruccion, tablaSimbolos)
        elif isinstance(instruccion, SContinue): intContinue(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FFor): intFFor(instruccion, tablaSimbolos)

        #print(type(DefFuncion))        
        elif isinstance(instruccion, DefFuncion): intDefFuncion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, DefFuncParam): intDefFuncParam(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FuncParams): intDefFuncParam(instruccion, tablaSimbolos)
        elif isinstance(instruccion, LlamadaFuncion): intLlamadaFuncion(instruccion, tablaSimbolos)
        else:
            print('TIPO -->', type(instruccion))



# -------------------------------------------------------------------------
# FUNCIONES ---------------------------------------------------------------
# -------------------------------------------------------------------------

def intDefFuncion(instr:DefFuncion, tablaSimbolos : cst.TablaSimbolos):
    print('DEFINICION DE UNA FUNCIÓN')
    pass

def intDefFuncParam(instr:DefFuncParam, tablaSimbolos : cst.TablaSimbolos):
    print('PARAMS DE DEFINICIÓN')
    pass

def intDefFuncParams(instr:FuncParams, tablaSimbolos : cst.TablaSimbolos):
    print('PARAMS DE UNA LLAMADA')
    pass

def intLlamadaFuncion(instr:LlamadaFuncion, tablaSimbolos : cst.TablaSimbolos):
    print('LLAMADA')
    pass


# -------------------------------------------------------------------------
# IMPRESION ---------------------------------------------------------------
# -------------------------------------------------------------------------
# region impresion -- revisada
def intImpresion(instr, tablaSimbolos: cst.TablaSimbolos):
    print('impresion')
    aux = ""
    global funcionusada
    global saltotrue
    global saltofalse
    global saltorest

    for instruccion in instr.texto:
        # tal vez le tenga que poner un if al res, pero una crisis a la vez xd
        funcionusada = 0

        res = resolverNumerica(instruccion, tablaSimbolos)
        global usandovars
        print('USANDOVARS: ', usandovars, ' CONTAVARS -> ', contavars)

        if funcionusada == 0: #numerica
            var = verificarT(res)
            txt = "\"%d\", int(" + var  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + var 
            aux += "fmt.Printf(" + txt + ");\n" 
        elif funcionusada == 1: #strings
            var = verificarT(res)

            global yaprintstring
            if not yaprintstring:
                yaprintstring = True

                temp1 = crearTemporal()
                temp2 = crearTemporal()
                temp3 = crearTemporal()

                salto1 = crearSalto()
                salto2 = crearSalto()
                y = ""

                y += temp1 + siwal+ getP("+1")
                y += temp2 + siwal + getStack(temp1) + fincomando  #pos en h del str temp               
                y += iniciarSalto(salto1) 
                y += temp3 + siwal + getHeap(temp2) + fincomando
                y += crearIf(temp3 + " == -1", salto2)
                y += "fmt.Printf(\"%c\", int(" + temp3 +"))" + fincomando
                y += tempmasmas(temp2)
                y += iniciarGoto(salto1)
                y += iniciarSalto(salto2)
                y += "return" + fincomando

                meterfuncion("imprimir", y)


            temp5 = crearTemporal()
            temp6 = crearTemporal()
            
            aux += temp5 + siwal + getP("+" + str(contavars))
            aux += tempmasmas(temp5)
            aux += getStack(temp5) + siwal + var + fincomando
            aux += aumentarP(contavars)
            aux += "imprimir()" + fincomando
            aux += temp6 + siwal + getStack("P") + fincomando
            aux += disminuirP(contavars)
        elif funcionusada == 2: #bools
            var = verificarT(res)

            if saltofalse == "" or saltotrue == "":
                saltotrue = crearSalto()
                saltofalse = crearSalto()
                saltorest = crearSalto()

            if var == False or 'alse' in var:
                var = "0"
            elif var == True or 'rue' in var:
                var = "1"

            if usandovars:
                aux += crearIf(var + " == 1", saltotrue)
                aux += iniciarGoto(saltofalse)

            aux += iniciarSalto(saltotrue)
            aux += meterPalabra("true")
            aux += iniciarGoto(saltorest)
            aux += iniciarSalto(saltofalse)
            aux += meterPalabra("false")
            aux += iniciarSalto(saltorest)      
        elif funcionusada == 3: #nothing
            aux += meterPalabra('nil')
        elif funcionusada == 4: #array
            var = verificarT(res)
            txt = "\"%d\", int(" + var  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + var 
            aux += "fmt.Printf(" + txt + ");\n"
        elif funcionusada == 5: # llamadaArray
            var = verificarT(res)
            nuevo = crearTemporal()
            aux += nuevo + siwal + getHeap(var) + fincomando

            txt = "\"%d\", int(" + nuevo  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + nuevo 
            aux += "fmt.Printf(" + txt + ");\n"



        instruccionesencero()
        saltofalse = ""
        saltotrue = ""
           
    meteraTraduccion(aux)   
    
def intImpresionLN(instr, tablaSimbolos : cst.TablaSimbolos):
    print('impresionLN')
    aux = ""
    global funcionusada
    global saltotrue
    global saltofalse
    global saltorest

    for instruccion in instr.texto:
        # tal vez le tenga que poner un if al res, pero una crisis a la vez xd
        funcionusada = 0

        res = resolverNumerica(instruccion, tablaSimbolos)
        global usandovars
        print('USANDOVARS: ', usandovars, ' CONTAVARS -> ', contavars)

        if funcionusada == 0: #numerica
            var = verificarT(res)
            txt = "\"%d\", int(" + var  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + var 
            aux += "fmt.Printf(" + txt + ");\n" 
        elif funcionusada == 1: #strings
            var = verificarT(res)

            global yaprintstring
            if not yaprintstring:
                yaprintstring = True

                temp1 = crearTemporal()
                temp2 = crearTemporal()
                temp3 = crearTemporal()

                salto1 = crearSalto()
                salto2 = crearSalto()
                y = ""

                y += temp1 + siwal+ getP("+1")
                y += temp2 + siwal + getStack(temp1) + fincomando  #pos en h del str temp               
                y += iniciarSalto(salto1) 
                y += temp3 + siwal + getHeap(temp2) + fincomando
                y += crearIf(temp3 + " == -1", salto2)
                y += "fmt.Printf(\"%c\", int(" + temp3 +"))" + fincomando
                y += tempmasmas(temp2)
                y += iniciarGoto(salto1)
                y += iniciarSalto(salto2)
                y += "return" + fincomando

                meterfuncion("imprimir", y)


            temp5 = crearTemporal()
            temp6 = crearTemporal()
            
            aux += temp5 + siwal + getP("+" + str(contavars))
            aux += tempmasmas(temp5)
            aux += getStack(temp5) + siwal + var + fincomando
            aux += aumentarP(contavars)
            aux += "imprimir()" + fincomando
            aux += temp6 + siwal + getStack("P") + fincomando
            aux += disminuirP(contavars)
        elif funcionusada == 2: #bools
            var = verificarT(res)

            if saltofalse == "" or saltotrue == "":
                saltotrue = crearSalto()
                saltofalse = crearSalto()
                saltorest = crearSalto()

            if var == False or 'alse' in var:
                var = "0"
            elif var == True or 'rue' in var:
                var = "1"

            if usandovars:
                aux += crearIf(var + " == 1", saltotrue)
                aux += iniciarGoto(saltofalse)

            aux += iniciarSalto(saltotrue)
            aux += meterPalabra("true")
            aux += iniciarGoto(saltorest)
            aux += iniciarSalto(saltofalse)
            aux += meterPalabra("false")
            aux += iniciarSalto(saltorest)           
        elif funcionusada == 3: #nothing
            aux += meterPalabra('nil')
        elif funcionusada == 4: #array
            var = verificarT(res)
            txt = "\"%d\", int(" + var  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + var 
            aux += "fmt.Printf(" + txt + ");\n"
        elif funcionusada == 5: # llamadaArray
            var = verificarT(res)
            nuevo = crearTemporal()
            aux += nuevo + siwal + getHeap(var) + fincomando

            txt = "\"%d\", int(" + nuevo  + ")"
            if "." in str(res) or "t" in str(res): 
                txt = "\"%f\", " + nuevo 
            aux += "fmt.Printf(" + txt + ");\n"

        instruccionesencero()
        saltofalse = ""
        saltotrue = ""
           
    aux += "fmt.Printf(\"%c\", 10)" + fincomando
    meteraTraduccion(aux)   
# endregion

# ------------------------------------------------------------------------- 
# DECLARACION -------------------------------------------------------------
# -------------------------------------------------------------------------
# region declaracion -- revisada

def intDeclaracion(instr:Asignacion, tablaSimbolos : cst.TablaSimbolos):
    print('Asignando en declaración')
    print(instr.nombre)
    print(instr.valor)

    global saltofalse
    global saltotrue
    global saltorest

    global pilaentornos
    global funcionusada
    ambito = pilaentornos[-1]

    valor = resolverNumerica(instr.valor, tablaSimbolos)
    aux = siExiste(instr.nombre, tablaSimbolos)
    
    tipo = "Undefined"
    if funcionusada == 0:
        tipo = "Numeric"
    elif funcionusada == 1:
        tipo = "String"
    elif funcionusada == 2:
        tipo = "Bool"
    elif funcionusada == 3:
        tipo = "Nil"
    elif funcionusada == 4:
        tipo = "Array"
    elif funcionusada == 5:
        tipo = "ArrayComponent"
 
    # si ya existe el coso en la ts
    if aux:
        print('actualizando')
        if aux.tipo == 'Function':
            errorEquis('Asignación', 'ya existe una funcion con este nombre')
            return ""

        # actualizo el valor      

        simbolo = cst.NodoSimbolo(instr.nombre, tipo, ambito, valor)
        simbolo.nota = 'Actualización'
        tablaSimbolos.actualizar(simbolo)
        #borrardeTabla(aux)
        #añadiraTabla(simbolo)

        x = ""
        posicion = aux.posicion
        if tipo == "Int64" or tipo == "Float64" or funcionusada == 0:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando        
        elif tipo == "Bool" or funcionusada == 2 :
            #print('-->', valor)
            if valor == "False" or valor == "false" or valor == False:
                valor = 0
            else:
                valor = 1
            x += getStack(posicion) + siwal + str(valor) + fincomando  
        elif tipo == "String" or funcionusada == 1 :
            posenH = crearTemporal()
            x += posenH + siwal + getH("")
            
            for i in valor:
                ascii = ord(i)
                x += getHeap("H") + siwal + str(ascii) + fincomando
                x += aumentarH(1)

            x += getHeap("H") + siwal + "-1" + fincomando
            x += aumentarH(1)

            x += getStack(posicion) + siwal + posenH + fincomando
        elif tipo == "None" or tipo == None or funcionusada == 3:
            x += getStack(posicion) + siwal + "0" + fincomando
        elif tipo == "Array" or tipo == None or funcionusada == 4:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando

        meteraTraduccion(x)
        return getStack(posicion)

    # si el valor es nuevo  
    else:
        print('nuevo')
        # creo una nueva variable
        posicion = crearposicion()

        simbolo = cst.NodoSimbolo(instr.nombre, tipo, ambito, posicion)
        tablaSimbolos.agregar(simbolo)
        #añadiraTabla(simbolo)

        #acá meto mi c3d

        x = ""
        if tipo == "Int64" or tipo == "Float64" or funcionusada == 0:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando        
        elif tipo == "Bool" or funcionusada == 2 :
            print('val-->', valor)
            if valor == "False" or valor == "false" or valor == False:
                valor = 0
            elif valor == "True" or valor == "true" or valor == True:
                valor = 1
            else: 
                valor = verificarT(valor)
            
            if saltofalse == "" or saltotrue == "":
                saltotrue = crearSalto()
                saltofalse = crearSalto()
                saltorest = crearSalto()
            
            x += metercomentario('inicio -- Para que funcione T.T')
            x += crearIf("0 != 0", saltofalse)
            x += iniciarGoto(saltotrue)
            x += metercomentario('fin -- Para que funcione T.T')

            x += iniciarSalto(saltotrue)
            x += getStack(posicion) + siwal + str(valor) + fincomando  
            x += iniciarGoto(saltorest)
            x += iniciarSalto(saltofalse)
            x += getStack(posicion) + siwal + "0" + fincomando
            x += iniciarSalto(saltorest)
        elif tipo == "String" or funcionusada == 1 :
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando
        elif tipo == "None" or tipo == None or funcionusada == 3:
            x += getStack(posicion) + siwal + "0" + fincomando
        elif tipo == "Array"  or funcionusada == 4:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando
        elif tipo == "ArrayComponent"  or funcionusada == 5:
            tempaux = crearTemporal()
            x += tempaux + siwal + getHeap(verificarT(valor)) + fincomando
            x += getStack(posicion) + siwal + tempaux + fincomando

        meteraTraduccion(x)
        global contavars
        contavars = contavars +1
        instruccionesencero()
        return getStack(posicion)

    return ""

def intScope(instr: Scope, tablaSimbolos : cst.TablaSimbolos):
    print('Asignando en scope')
    print(instr.asignacion.nombre)
    print(instr.asignacion.valor)

    global saltofalse
    global saltotrue
    global saltorest

    global pilaentornos
    global funcionusada
    ambito = pilaentornos[-1]
    if instr.scope == 'global':
        ambito = 'global'
    asignacion = instr.asignacion

    # CAMBIOS A LA IQUIERDA
    try: 
    #si lo que está a la izq es un array 
        if isinstance(instr.asignacion.nombre, LlamadaArr):
            print('ARRAY A LA IZQUIERDA')
            indiceHeap = resolverNumerica(instr.asignacion.nombre, tablaSimbolos) 

            valor = resolverNumerica(asignacion.valor, tablaSimbolos)

            global funcionusada
            tipo = "Undefined"
            if funcionusada == 0:
                tipo = "Numeric"
            elif funcionusada == 1:
                tipo = "String"
            elif funcionusada == 2:
                tipo = "Bool"
            elif funcionusada == 3:
                tipo = "Nil"
            elif funcionusada == 4:
                tipo = "Array"
            elif funcionusada == 5:
                tipo = "ArrayComponent"

            # si es tipada
            if asignacion.tipo != "":
                tipo = asignacion.tipo.id
                if tipo != tipoVariable(valor):
                    if tipo == "Int64" and funcionusada == 0:
                        pass
                    elif tipo == "Foat64" and funcionusada == 0:
                        pass
                    else:
                        errordeTipos("Declaración de " + asignacion.nombre[0].id)
                        return ""
            izquierda = getHeap(verificarT(indiceHeap))
            x = ""
            if tipo == "Int64" or tipo == "Float64" or funcionusada == 0:
                x += izquierda + siwal + verificarT(valor) + fincomando        
            elif tipo == "Bool" or funcionusada == 2 :
                print('val-->', valor)
                if valor == "False" or valor == "false" or valor == False:
                    valor = 0
                elif valor == "True" or valor == "true" or valor == True:
                    valor = 1
                else: 
                    valor = verificarT(valor)
                
                if saltofalse == "" or saltotrue == "":
                    saltotrue = crearSalto()
                    saltofalse = crearSalto()
                    saltorest = crearSalto()
                
                x += metercomentario('inicio -- Para que funcione T.T')
                x += crearIf("0 != 0", saltofalse)
                x += iniciarGoto(saltotrue)
                x += metercomentario('fin -- Para que funcione T.T')

                x += iniciarSalto(saltotrue)
                x += izquierda + siwal + str(valor) + fincomando  
                x += iniciarGoto(saltorest)
                x += iniciarSalto(saltofalse)
                x += izquierda + siwal + "0" + fincomando
                x += iniciarSalto(saltorest)
            elif tipo == "String" or funcionusada == 1 :
                x += izquierda + siwal + verificarT(valor) + fincomando
            elif tipo == "None" or tipo == None or funcionusada == 3:
                x += izquierda + siwal + "0" + fincomando
            elif tipo == "Array"  or funcionusada == 4:
                x += izquierda + siwal + verificarT(valor) + fincomando
            elif tipo == "ArrayComponent"  or funcionusada == 5:
                tempaux = crearTemporal()
                x += tempaux + siwal + getHeap(verificarT(valor)) + fincomando
                x += izquierda + siwal + tempaux + fincomando

            meteraTraduccion(x)
            return ""         
    except Exception as ee:
        errorEquis('Asignación', 'algo x pasó :c' + ee)
    
    # SIN CAMBIOS A LA IQUIERDA
    valor = resolverNumerica(asignacion.valor, tablaSimbolos)    
    aux = siExiste(asignacion.nombre[0].id, tablaSimbolos)

    tipo = "Undefined"
    if funcionusada == 0:
        tipo = "Numeric"
    elif funcionusada == 1:
        tipo = "String"
    elif funcionusada == 2:
        tipo = "Bool"
    elif funcionusada == 3:
        tipo = "Nil"
    elif funcionusada == 4:
        tipo = "Array"
    elif funcionusada == 5:
        tipo = "ArrayComponent"

    # si es tipada
    if asignacion.tipo != "":
        tipo = asignacion.tipo.id
        if tipo != tipoVariable(valor):
            if tipo == "Int64" and funcionusada == 0:
                pass
            elif tipo == "Foat64" and funcionusada == 0:
                pass
            else:
                errordeTipos("Declaración de " + asignacion.nombre[0].id)
                return ""
    
    # si ya existe el coso en la ts
    if aux:
        print('actualizando')
        if aux.tipo == 'Function':
            errorEquis('Asignación', 'ya existe una funcion con este nombre')
            return ""

        # actualizo el valor
        simbolo = cst.NodoSimbolo(asignacion.nombre[0].id, tipo, ambito, aux.posicion)
        simbolo.nota = 'Actualizado'
        tablaSimbolos.actualizar(simbolo)
        borrardeTabla(aux)
        añadiraTabla(simbolo)

        x = ""
        posicion = aux.posicion
        if tipo == "Int64" or tipo == "Float64" or funcionusada == 0:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando        
        elif tipo == "Bool" or funcionusada == 2 :
            #print('-->', valor)
            if valor == "False" or valor == "false" or valor == False:
                valor = 0
            else:
                valor = 1
            x += getStack(posicion) + siwal + str(valor) + fincomando  
        elif tipo == "String" or funcionusada == 1 :
            #posenH = crearTemporal()
            #x += posenH + siwal + getH("")
            
            #for i in valor:
            #    ascii = ord(i)
            #    x += getHeap("H") + siwal + str(ascii) + fincomando
            #    x += aumentarH(1)

            #x += getHeap("H") + siwal + "-1" + fincomando
            #x += aumentarH(1)

            x += getStack(posicion) + siwal + valor + fincomando
        elif tipo == "None" or tipo == None or funcionusada == 3:
            x += getStack(posicion) + siwal + "0" + fincomando
        elif tipo == "Array" or tipo == None or funcionusada == 4:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando

        meteraTraduccion(x)
        return ""

    # si el valor es nuevo  
    else:
        print('nuevo')
        # creo una nueva variable
        posicion = crearposicion()

        simbolo = cst.NodoSimbolo(asignacion.nombre[0].id, tipo, ambito, posicion)
        tablaSimbolos.agregar(simbolo)
        añadiraTabla(simbolo)

        #acá meto mi c3d

        x = ""
        if tipo == "Int64" or tipo == "Float64" or funcionusada == 0:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando        
        elif tipo == "Bool" or funcionusada == 2 :
            print('val-->', valor)
            if valor == "False" or valor == "false" or valor == False:
                valor = 0
            elif valor == "True" or valor == "true" or valor == True:
                valor = 1
            else: 
                valor = verificarT(valor)
            
            if saltofalse == "" or saltotrue == "":
                saltotrue = crearSalto()
                saltofalse = crearSalto()
                saltorest = crearSalto()
            
            x += metercomentario('inicio -- Para que funcione T.T')
            x += crearIf("0 != 0", saltofalse)
            x += iniciarGoto(saltotrue)
            x += metercomentario('fin -- Para que funcione T.T')

            x += iniciarSalto(saltotrue)
            x += getStack(posicion) + siwal + str(valor) + fincomando  
            x += iniciarGoto(saltorest)
            x += iniciarSalto(saltofalse)
            x += getStack(posicion) + siwal + "0" + fincomando
            x += iniciarSalto(saltorest)
        elif tipo == "String" or funcionusada == 1 :
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando
        elif tipo == "None" or tipo == None or funcionusada == 3:
            x += getStack(posicion) + siwal + "0" + fincomando
        elif tipo == "Array"  or funcionusada == 4:
            x += getStack(posicion) + siwal + verificarT(valor) + fincomando
        elif tipo == "ArrayComponent"  or funcionusada == 5:
            tempaux = crearTemporal()
            x += tempaux + siwal + getHeap(verificarT(valor)) + fincomando
            x += getStack(posicion) + siwal + tempaux + fincomando

        meteraTraduccion(x)
        global contavars
        contavars = contavars +1
        instruccionesencero()
        return ""
  
# endregion

# ------------------------------------------------------------------------- 
# CONDICIONALES -----------------------------------------------------------
# ------------------------------------------------------------------------- 

# region if - revisada
def intFIF(instr, tablaSimbolos : cst.TablaSimbolos):
    print('IF')

    global pilaentornos
    global saltotrue
    global saltofalse
    global saltorest

    pilaentornos.append('if')
    print('oplog', instr.oplog)
    print('instruccionesv : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global
    aux = ""

    tempdecisivo = resolverBooleana(instr.oplog, tablaSimbolos)
    if saltofalse == "" or saltotrue == "":
        saltotrue = crearSalto()
        saltofalse = crearSalto()
        saltorest = crearSalto()

    truetemp = saltotrue
    falsetemp = saltofalse
    resttemp = saltorest

    aux += iniciarSalto(truetemp)    
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando if true')
    meteraTraduccion(aux)
    procesarInstrucciones(instr.instruccionesv, ts_local)

    aux = iniciarGoto(resttemp)
    aux += iniciarSalto(falsetemp)
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando if false')
    meteraTraduccion(aux)
    procesarInstrucciones([instr.instruccionesf], ts_local)

    aux = metercomentario('fin de if')
    aux += iniciarSalto(resttemp)
    
    meteraTraduccion(aux)
    pilaentornos.pop()

def intFElseIF(instr, tablaSimbolos : cst.TablaSimbolos):
    print('elif')

    global pilaentornos
    global saltotrue
    global saltofalse
    global saltorest

    pilaentornos.append('elif')
    print('oplog', instr.oplog)
    print('instrucciones : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global
    aux = ""

    tempdecisivo = resolverBooleana(instr.oplog, tablaSimbolos)
    if saltofalse == "" or saltotrue == "":
        saltotrue = crearSalto()
        saltofalse = crearSalto()
        saltorest = crearSalto()

    truetemp = saltotrue
    falsetemp = saltofalse
    resttemp = saltorest

    aux += iniciarSalto(truetemp)    
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando elseif true')
    meteraTraduccion(aux)
    procesarInstrucciones(instr.instruccionesv, ts_local)

    aux = iniciarGoto(resttemp)
    aux += iniciarSalto(falsetemp)
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando elseif false')
    meteraTraduccion(aux)
    procesarInstrucciones([instr.instruccionesf], ts_local)

    aux = metercomentario('fin de if')
    aux += iniciarSalto(resttemp)
    
    meteraTraduccion(aux)
    pilaentornos.pop()

def intFELSE(instr, tablaSimbolos : cst.TablaSimbolos):
    print('else')

    global pilaentornos
    pilaentornos.append('else')

    global ts_global
    ts_local = ts_global

    procesarInstrucciones(instr.instrucciones, ts_local)

    pilaentornos.pop()

def intFIFuni(instr, tablaSimbolos : cst.TablaSimbolos):
    print('if')

    global pilaentornos
    global saltotrue
    global saltofalse
    global saltorest
    pilaentornos.append('if')
    print('oplog', instr.oplog)
    print('instruccionesv : ', instr.instruccionesv)
    print('instruccionesf : ', instr.instruccionesf)

    global ts_global
    ts_local = ts_global
    aux = ""

    tempdecisivo = resolverBooleana(instr.oplog, tablaSimbolos)
    if saltofalse == "" or saltotrue == "":
        saltotrue = crearSalto()
        saltofalse = crearSalto()
        saltorest = crearSalto()

    truetemp = saltotrue
    falsetemp = saltofalse
    resttemp = saltorest

    aux += iniciarSalto(truetemp)    
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando if true')
    meteraTraduccion(aux)
    procesarInstrucciones(instr.instruccionesv, ts_local)

    aux = iniciarGoto(resttemp)
    aux += iniciarSalto(falsetemp)
    #acá resuelvo las instrucciones si son true
    aux += metercomentario('iniciando if false')
    meteraTraduccion(aux)
    procesarInstrucciones([instr.instruccionesf], ts_local)

    aux = metercomentario('fin de if')
    aux += iniciarSalto(resttemp)
    
    meteraTraduccion(aux)
    pilaentornos.pop()

# endregion

# region while for - en proceso
def intFWhile(instr : FWhile, tablaSimbolos : cst.TablaSimbolos):
    print('while')

    global pilaentornos
    global saltofalse
    global saltorest
    global saltotrue

    pilaentornos.append('while')
    print('oplog', instr.oplog)
    #print('instrucciones : ', instr.instrucciones)

    global ts_global
    ts_local = ts_global

    saltowhile = crearSalto() #este es el salto inicial inicial
    global inicioloop
    inicioloop = saltowhile

    z = metercomentario("iniciando while")
    z += iniciarSalto(saltowhile)
    meteraTraduccion(z)

    tempdecisivo = resolverBooleana(instr.oplog, tablaSimbolos)
    if saltofalse == "" or saltotrue == "":
        saltotrue = crearSalto()
        saltofalse = crearSalto()
        saltorest = crearSalto()

    truetemp = saltotrue
    falsetemp = saltofalse
    resttemp = saltorest
    global findeloop
    findeloop = falsetemp
    print('SALTOS ', inicioloop , ' , ', findeloop )

    z = iniciarSalto(truetemp)
    meteraTraduccion(z)

    procesarInstrucciones(instr.instrucciones, ts_local)

    z = iniciarGoto(saltowhile)
    z += iniciarSalto(falsetemp)
    
    meteraTraduccion(z)       

    pilaentornos.pop()
    inicioloop = ""
    findeloop = ""

def intBreak(instr: SBreak, tablaSimbolos: cst.TablaSimbolos):
    global inicioloop
    global findeloop
    print('CONTINUE ', inicioloop , ' , ', findeloop) 

    if inicioloop == "" or findeloop == "":
        errorEquis('Break', 'No se encuentra en un loop')
        return

    x = ""
    x += metercomentario("Break")
    x += iniciarGoto(findeloop)
    meteraTraduccion(x)

def intContinue(instr: SBreak, tablaSimbolos: cst.TablaSimbolos):
    global inicioloop
    global findeloop
    print('CONTINUE ', inicioloop , ' , ', findeloop)    

    if inicioloop == "" or findeloop == "":
        errorEquis('Continue', 'No se encuentra en un loop')
        return

    x = ""
    x += metercomentario("Continue")
    x += iniciarGoto(inicioloop)
    meteraTraduccion(x)

def intFFor(instr: FFor, tablaSimbolos : cst.TablaSimbolos):

    print('for')
    global pilaentornos
    global contavars
    global funcionusada
    global ts_global
    ts_local = ts_global
    pilaentornos.append('for')

    print('Instrucciones', instr.instrucciones)
    print('id =', instr.var)
    print('rangoraw21', instr.rango)
    #temp2 = intDeclaracion(Asignacion("temp", instr.rango), tablaSimbolos)
    # temp2 es un temporal que me dice donde está mi rango

    temp2 = resolverNumerica(instr.rango, tablaSimbolos)
    # el rango puede ser un array, o un id, el temp2 me dice cual es el tamaño del coso
    print('rangoraw2 ', temp2, ' funcionusada ', funcionusada)

    temp3 = crearTemporal()
    temp4 = crearTemporal()
    temp5 = crearTemporal()
    temp6 = crearTemporal()
    temp7 = crearTemporal()
    temp9 = crearTemporal()
    temp8 = crearTemporal()    
    temp10 = crearTemporal()
    

    saltoinicial = crearSalto()
    saltointermedio = crearSalto()
    saltofinal = crearSalto()

    x = metercomentario('FOR')
    x += metercomentario("Mi Rango:")

    x += temp3 + siwal + getHeap(verificarT(temp2)) + fincomando #tamaño del coso si es array

    x += temp4 + siwal + "0" + fincomando #la iteración empieza en el 0

    #x += tempmasmas(temp2)
    x += temp5 + siwal + aumentartemp(temp4, verificarT(temp2)) # posicion del arr en heap

    #x += tempmasmas(temp5) # donde empiezan los valores del arr
    meteraTraduccion(x)

    #acá declaro la variable?
    x = metercomentario("declarando la variable del for")
    meteraTraduccion(x)
    posaux = intDeclaracion(Asignacion(instr.var, OPNum(0)), tablaSimbolos)    
    # declaro la variable vacía
    x = tempmasmas(temp5)
    x += temp6 + siwal + getHeap(verificarT(temp5)) + fincomando #geteo el primer valor del arr
    #x += temp7 + siwal + getP("+" + str(contavars)) #un lugar vació en stack
    #x += getStack(temp7) + siwal + verificarT(temp6) + fincomando# el lugar vacio en el stack es el primer del arr
    x += posaux + siwal + verificarT(temp6) + fincomando# el lugar vacio en el stack es el primer del arr


    x += iniciarSalto(saltoinicial)
    x += crearIf(temp4 + " == "+ temp3, saltofinal) #si el contador es iwal al tamaño del coso muerte

    x += temp9 + siwal + getP("+" + str(contavars)) #el lugar donde está guardado el primero del arr
    meteraTraduccion(x)

    procesarInstrucciones(instr.instrucciones, ts_local)

    x = metercomentario('después de las instruccions')
    #x += iniciarSalto(saltointermedio)
    x += tempmasmas(temp4) # aumento en la iteración
    x += tempmasmas(temp5) # agarro el siguiente del array
    x += temp6 + siwal + getHeap(temp5) + fincomando # agarro el siguiente del arrx2
    x += posaux + siwal + temp6 + fincomando # el lugar vacio en el stack es el .. del arr
    x += iniciarGoto(saltoinicial)

    x += iniciarSalto(saltofinal)
    meteraTraduccion(x)

    


# endregion

# ------------------------------------------------------------------------- 
# OPERACIONES -------------------------------------------------------------
# ------------------------------------------------------------------------- 

# region operaciones - revisada
def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    global smas
    global smenos
    global fincomando
    global siwal
    global funcionusada
    funcionusada = 0
    global usandovars

    if isinstance(Exp, OPNum):
        
        if Exp.val == 0:
            temp = crearTemporal()
            x = temp + siwal + '0' + fincomando
            meteraTraduccion(x)
            return x
        return Exp.val
    elif isinstance(Exp, OPBinaria): 
        
        print('RESOLVIENDO BINARIA')
        print(Exp.term1, ' ', Exp.operador, ' ' ,Exp.term2)
        if isinstance(Exp.term1, OPCadena) or isinstance(Exp.term2, OPCadena):
            x = resolverCadena(Exp, tablaSimbolos)
            return x
        
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos) 

        print('-->', funcionusada)
        if funcionusada != 0:
            print('oops, es otra binaria i')
            usandovars = usandovars -2 # quitando las vars de exp1 y exp2
            borrartemporal()
            borrartemporal()

            x = resolverCadena(Exp, tablaSimbolos)

            return x

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
            x += meterPalabra("MathError\n")
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
            aux =  siwal + getP("+" + str(contavars))
            aux2 =  siwal + getP("-" + str(contavars) )
            
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
            z = crearTemporal() + "=" + getStack(str(x.posicion)) + fincomando
            meteraTraduccion(z)
            
            usandovars = usandovars +1

            tipo = tipoEnTabla(x.posicion, tablaSimbolos)
            if tipo == "String":
                print('es-string ', 'usandovars: ', usandovars, ' funcionusada ', funcionusada)
                funcionusada = 1                
            elif tipo == "Int64" or tipo == "Float64" or tipo == "Numeric":
                print('es-numeric ', 'usandovars: ', usandovars, ' funcionusada ', funcionusada)
                funcionusada = 0                
            elif tipo == "Nil":
                print('es-nil ', 'usandovars: ', usandovars, ' funcionusada ', funcionusada)
                funcionusada = 3                
            elif tipo == "Bool":
                print('es-bool ', 'usandovars: ', usandovars, ' funcionusada ', funcionusada)
                funcionusada = 2
            elif tipo == "Array":
                print('es-array ', 'usandovars: ', usandovars, ' funcionusada ', funcionusada)
                funcionusada = 4
            return z                
        else: 
            print('FALLA EN ID')
            return "0"
    elif isinstance(Exp, OPNothing):
        print('OPNOTHING')
        funcionusada = 3
        return "0"
    
    elif isinstance(Exp, OPType):
        return ""
    elif isinstance(Exp, list):
        print('Acá hay un arreglo')        
        x = ""

        tamaño = len(Exp)      

        if isinstance(Exp[0], OPNothing):
            tamaño = 0

        temp0 = crearTemporal()
        temp1 = crearTemporal()

        x += temp0 + siwal + getH("") # donde empieza el array
        x += getHeap("H") + siwal + str(tamaño) + fincomando #heap de donde empieza = el tamaño
        x += temp1 + siwal + aumentartemp(temp0, str(1)) #donde meto el primer cosito  t1 = h+1
        x += aumentarH(tamaño + 1) + "\n"#reservando el tamaño del arreglo

        #en teoría, h ya es x para este arreglo, no importa        
        for term in Exp:
            if isinstance(term, OPNothing):
                break

            term = resolverNumerica(term, tablaSimbolos)

            x += getHeap(temp1) + siwal + verificarT(term) + fincomando
            x += tempmasmas(temp1)

        meteraTraduccion(x)
        funcionusada = 4
        print('terminando arreglo')
        return temp0
    elif isinstance(Exp, LlamadaArr):
        print('Acá hay una llamada arr')
        print(Exp.nombre)
        print(Exp.inds)

        arr_indices = []
        contadimensiones = 0
        for indice in Exp.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if funcionusada != 0:
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(Exp.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        funcionusada = 4

        temp8 = crearTemporal()
        temp9 = crearTemporal()
        
        
        z = temp8 + siwal + getStack(str(arr.posicion)) + fincomando
        usandovars = usandovars +1
        meteraTraduccion(z) 
        
        try:
            if contadimensiones == 0: 
                checarIndice("-1", "0", "0")                
                return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                x = metercomentario("arr de una dimensión")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                #x += temp10 + siwal + getHeap(temp9) + fincomando

                meteraTraduccion(x)
                funcionusada = 5
                return temp9
            elif contadimensiones == 2:
                temp10 = crearTemporal()
                temp11 = crearTemporal()
                #temp12 = crearTemporal()

                x = metercomentario("arr de dos dimensiones")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                x += temp10 + siwal + getHeap(temp9) + fincomando

                
                x += checarIndice(verificarT(arr_indices[1]), temp10)
                x += temp11 + siwal + aumentartemp(temp10, verificarT(arr_indices[1]))
                x += tempmasmas(temp11)
                #x += temp12 + siwal + getHeap(temp11) + fincomando

                meteraTraduccion(x)
                funcionusada = 5
                return temp11
            elif contadimensiones == 3: 
                temp10 = crearTemporal()
                temp11 = crearTemporal()
                temp12 = crearTemporal()
                temp13 = crearTemporal()

                x = metercomentario("arr de tres dimensiones")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                x += temp10 + siwal + getHeap(temp9) + fincomando

                x += checarIndice(verificarT(arr_indices[1]), temp10)
                x += temp11 + siwal + aumentartemp(temp10, verificarT(arr_indices[1]))
                x += tempmasmas(temp11)
                x += temp12 + siwal + getHeap(temp11) + fincomando

                x += checarIndice(verificarT(arr_indices[2]), temp12)
                x += temp13 + siwal + aumentartemp(temp12, verificarT(arr_indices[2]))
                x += tempmasmas(temp13)

                meteraTraduccion(x)
                funcionusada = 5
                return temp13
        except Exception as e:
            print(e)
            return errorEquis('Llamada a valor de arreglo', str(e))

    # FORS
    elif isinstance(Exp, FForRangoNum):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        print('RANGOS: ', exp1, exp2)

        tempmenor = crearTemporal()
        tempmayor = crearTemporal()
        temptamanio = crearTemporal()
        temp0 = crearTemporal()
        temp1 = crearTemporal()
        saltoinicio = crearSalto()
        saltofinal = crearSalto()

        y = metercomentario("generando array")
        y += tempmenor + siwal + verificarT(exp1) + fincomando#1
        y += tempmayor + siwal + verificarT(exp2) + fincomando  #3   
        y += temptamanio + siwal + "0" + fincomando      
            
        y += temp0 + siwal + getH("")
        y += temp1 + siwal + aumentartemp(temp0, "1")
        y += aumentarH(1) #guardo el lugar para el espacio

        y += iniciarSalto(saltoinicio)
        y += crearIf(tempmenor + " > " + tempmayor, saltofinal)

        y += getHeap(temp1) + siwal + tempmenor + fincomando
        y += aumentarH(1)
        y += temp1 + siwal + aumentartemp(temp1, "1")        

        y += tempmenor + siwal + aumentartemp(tempmenor, "1")
        y += temptamanio + siwal + aumentartemp(temptamanio, "1")
        y += iniciarGoto(saltoinicio)
        y += iniciarSalto(saltofinal)


        y += getHeap(temp0) + siwal + temptamanio + fincomando # este es el tamaño

        meteraTraduccion(y)
        return temp0

    elif isinstance(Exp, LlamadaFuncion): 
        return ""   
    else: 
        print('viendo si se va a las cadenas, ', Exp)
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return ""
        return resolverCadena(Exp, tablaSimbolos)

def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    global funcionusada 
    funcionusada = 1
    global usandovars

    if isinstance(Exp, OPBinaria):
        print('RESOLVIENDO CADENA BINARIA')
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        if Exp.operador == ARITMETICA.ASTERISCO : 
            funcionusada = 1
            # HACIENDO LA FUNCION
            global yaconcatstring
            if not yaconcatstring:
                temp3 = crearTemporal()
                temp4 = crearTemporal()
                temp6 = crearTemporal()
                temp5 = crearTemporal() 
                temp7 = crearTemporal()     

                salto1 = crearSalto()
                salto2 = crearSalto()
                salto3 = crearSalto()
                salto4 = crearSalto()                          

                y = temp3 + siwal + getH("")
                y += temp4 + siwal + getP("+1") #cambio de ambito
                y += temp6 + siwal + getStack(temp4) + fincomando #el stack de la 1 palabra, pos en h de la 1
                y += temp5 + siwal + getP("+2") #cambiando de ambito x2
                y += iniciarSalto(salto1)
                y += temp7 + siwal + getHeap(temp6) + fincomando #inicio de la 1
                y += crearIf(temp7 + " == -1", salto2)
                y += getHeap("H") + siwal + temp7 + fincomando #copio la palabra 1 al heap
                y += aumentarH(1)
                y += tempmasmas(temp6) #aumento el temp que mira la posicion de las palabras
                y += iniciarGoto(salto1)
                y += iniciarSalto(salto2)
                y += temp6 + siwal + getStack(temp5) + fincomando #si ya termino la 1, me posiciono en el principio de la 2
                y += iniciarSalto(salto3) #1* letra de la 2
                y += temp7 + siwal + getHeap(temp6) + fincomando
                y += crearIf(temp7 + " == -1", salto4)
                y += getHeap("H") + siwal + temp7 +fincomando #copio la 2* donde me quedé hast arriba del heap
                y += aumentarH(1)
                y += tempmasmas(temp6)
                y += iniciarGoto(salto3)
                y += iniciarSalto(salto4) #si ya terminé las 2 palabras
                y += getHeap("H") + siwal + "-1" + fincomando #meto el fin de las 2 palabras
                y += aumentarH(1)
                y += getStack("P") + siwal + temp3 + fincomando #stack del nuevo es el inicio de H
                y += "return" + fincomando


                meterfuncion("concatenarStr", y)
                yaconcatstring = True

            # HACIENDO LO QUE VA EN EL MAIN

            temp8 = crearTemporal()
            temp9 = crearTemporal()


            x = temp8 + siwal + getP("+" + str(contavars)) #cambio de ambito (?)
            x += tempmasmas(temp8) 
            x += getStack(temp8) + siwal + verificarT(exp1) + fincomando #posicion de str1
            x += tempmasmas(temp8)
            x += getStack(temp8) + siwal + verificarT(exp2) + fincomando #pos de str2
            x += aumentarP(contavars)
            x += "concatenarStr()" + fincomando
            x += temp9 + siwal + getStack("P") + fincomando# acá es donde guardé el inicio del string concatenado
            x += disminuirP(contavars)
            meteraTraduccion(x)

            return temp9
        if Exp.operador == ARITMETICA.ELEVADO: # and tipoVariable(exp2) == 'Int64' and exp2 != None: 
            funcionusada = 1
            print('Es elevado al: ', exp2)
            # HACIENDO LA FUNCION
            if not yaconcatstring:
                temp3 = crearTemporal()
                temp4 = crearTemporal()
                temp6 = crearTemporal()
                temp5 = crearTemporal() 
                temp7 = crearTemporal()     

                salto1 = crearSalto()
                salto2 = crearSalto()
                salto3 = crearSalto()
                salto4 = crearSalto()                          

                y = temp3 + siwal + getH("")
                y += temp4 + siwal + getP("+1") #cambio de ambito
                y += temp6 + siwal + getStack(temp4) + fincomando #el stack de la 1 palabra, pos en h de la 1
                y += temp5 + siwal + getP("+2") #cambiando de ambito x2
                y += iniciarSalto(salto1)
                y += temp7 + siwal + getHeap(temp6) + fincomando #inicio de la 1
                y += crearIf(temp7 + " == -1", salto2)
                y += getHeap("H") + siwal + temp7 + fincomando #copio la palabra 1 al heap
                y += aumentarH(1)
                y += tempmasmas(temp6) #aumento el temp que mira la posicion de las palabras
                y += iniciarGoto(salto1)
                y += iniciarSalto(salto2)
                y += temp6 + siwal + getStack(temp5) + fincomando #si ya termino la 1, me posiciono en el principio de la 2
                y += iniciarSalto(salto3) #1* letra de la 2
                y += temp7 + siwal + getHeap(temp6) + fincomando
                y += crearIf(temp7 + " == -1", salto4)
                y += getHeap("H") + siwal + temp7 +fincomando #copio la 2* donde me quedé hast arriba del heap
                y += aumentarH(1)
                y += tempmasmas(temp6)
                y += iniciarGoto(salto3)
                y += iniciarSalto(salto4) #si ya terminé las 2 palabras
                y += getHeap("H") + siwal + "-1" + fincomando #meto el fin de las 2 palabras
                y += aumentarH(1)
                y += getStack("P") + siwal + temp3 + fincomando #stack del nuevo es el inicio de H
                y += "return" + fincomando


                meterfuncion("concatenarStr", y)
                yaconcatstring = True

            # HACIENDO LO QUE VA EN EL MAIN

            temp8 = crearTemporal() #el de la string
            aux = exp1
            for x in range(exp2-1):

                temp9 = crearTemporal()
                print('metiendo a ', temp9)
                x = temp8 + siwal + getP("+" + str(contavars)) #cambio de ambito (?)
                x += tempmasmas(temp8) 
                x += getStack(temp8) + siwal + verificarT(exp1) + fincomando #posicion de str1
                x += tempmasmas(temp8)

                x += getStack(temp8) + siwal + verificarT(aux) + fincomando #pos de str2
                x += aumentarP(contavars)
                x += "concatenarStr()" + fincomando
                x += temp9 + siwal + getStack("P") + fincomando# acá es donde guardé el inicio del string concatenado
                x += disminuirP(contavars)
                meteraTraduccion(x)
                exp1 = temp9

            return temp9
    elif isinstance(Exp, OPCadena):
        temp, trad = stringaHeap(Exp.id)
        meteraTraduccion(trad)
        return temp
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

        global yalowercase
        if not yalowercase:
            yalowercase = True
            temp2 = crearTemporal()
            temp3 = crearTemporal()
            temp4 = crearTemporal()
            salto0 = crearSalto()
            salto1 = crearSalto()
            salto2 = crearSalto()

            y = temp2 + siwal + getH("")
            y += temp3 + siwal + getP("+1")
            y += temp3 + siwal + getStack(temp3) + fincomando
            y += iniciarSalto(salto0)
            y += temp4 + siwal + getHeap(temp3) + fincomando
            y += crearIf(temp4 + " == -1", salto2)
            y += crearIf(temp4 + " < 65", salto1)
            y += crearIf(temp4 + " > 90", salto1)
            y += temp4 + siwal + temp4 + " + 32" + fincomando
            y += iniciarSalto(salto1)
            y += getHeap("H") + siwal + temp4 + fincomando
            y += aumentarH(1)
            y += tempmasmas(temp3)
            y += iniciarGoto(salto0)
            y += iniciarSalto(salto2)
            y += getHeap("H") + siwal + " -1" + fincomando
            y += aumentarH(1)
            y += getStack("P") + siwal + temp2 + fincomando
            y += "return" + fincomando

            meterfuncion("lowercase", y)

        temp1 = resolverCadena(Exp.term1, tablaSimbolos)

        temp6 = crearTemporal()
        temp7 = crearTemporal()

        x = temp6 + siwal + getP("+" + str(contavars)) #cambio de ambito (?)
        x += tempmasmas(temp6)
        x += getStack(temp6) + siwal + verificarT(temp1) + fincomando
        x += aumentarP(contavars)
        x += "lowercase()" + fincomando
        x += temp7 + siwal + getStack("P") + fincomando
        x += disminuirP(contavars)
        meteraTraduccion(x)
        
        return temp7
    elif isinstance(Exp, OPUppercase):

        global yauppercase
        if not yauppercase:
            yauppercase = True
            temp2 = crearTemporal()
            temp3 = crearTemporal()
            temp4 = crearTemporal()
            salto0 = crearSalto()
            salto1 = crearSalto()
            salto2 = crearSalto()

            y = temp2 + siwal + getH("")
            y += temp3 + siwal + getP("+1")
            y += temp3 + siwal + getStack(temp3) + fincomando
            y += iniciarSalto(salto0)
            y += temp4 + siwal + getHeap(temp3) + fincomando
            y += crearIf(temp4 + " == -1", salto2)
            y += crearIf(temp4 + " < 97", salto1)
            y += crearIf(temp4 + " > 122", salto1)
            y += temp4 + siwal + temp4 + " - 32" + fincomando
            y += iniciarSalto(salto1)
            y += getHeap("H") + siwal + temp4 + fincomando
            y += aumentarH(1)
            y += tempmasmas(temp3)
            y += iniciarGoto(salto0)
            y += iniciarSalto(salto2)
            y += getHeap("H") + siwal + " -1" + fincomando
            y += aumentarH(1)
            y += getStack("P") + siwal + temp2 + fincomando
            y += "return" + fincomando


            meterfuncion("uppercase", y)

        temp1 = resolverCadena(Exp.term1, tablaSimbolos)
                
        temp6 = crearTemporal()
        temp7 = crearTemporal()

        x = temp6 + siwal + getP("+" + str(contavars)) #cambio de ambito (?)
        x += tempmasmas(temp6)
        x += getStack(temp6) + siwal + verificarT(temp1) + fincomando
        x += aumentarP(contavars)
        x += "uppercase()" + fincomando
        x += temp7 + siwal + getStack("P") + fincomando
        x += disminuirP(contavars)
        meteraTraduccion(x)
        
        return temp7
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

def resolverBooleana(Exp, tablaSimbolos: cst.TablaSimbolos):
    global funcionusada 
    global saltofalse
    global saltotrue
    global saltorest
    global usandologica
    global comparandocadenas
    global contavars
    global yacomparestrings
    global usandovars
    funcionusada = 2

    if isinstance(Exp, OPLogica): 
        print('RESOLVIENDO LOGICA')
        print(Exp.term1, ' ', Exp.term2)
        permiso = True

        if Exp.operador == LOGICA.AND :
            usandologica.append(0)
            print('ES UN AND')
        elif Exp.operador == LOGICA.OR : 
            usandologica.append(1)
            print('ES UN OR')

        exp1 = resolverBooleana(Exp.term1, tablaSimbolos)

        if saltofalse == "" or saltotrue == "":
            saltotrue = crearSalto()
            saltofalse = crearSalto()
            saltorest = crearSalto()
        elif usandologica[-1] == 0:
            x = iniciarSalto(saltotrue)
            meteraTraduccion(x)
            saltotrue = crearSalto()
        elif usandologica[-1] == 1:
            x = iniciarSalto(saltofalse)
            meteraTraduccion(x)
            saltofalse = crearSalto()


        exp2 = resolverBooleana(Exp.term2, tablaSimbolos) 

        if exp1  == True or exp1 == False:
            pass
        else:
            print('-->', exp1, ' ', exp2, ' log: ', usandologica )

        #no se muestran
        if Exp.operador == LOGICA.AND : 
            print('poping ', usandologica[-1], ' ', usandologica)
            usandologica.pop(-1)
            permiso = False
            return exp1 and exp2
        elif Exp.operador == LOGICA.OR : 
            print('poping ', usandologica[-1], ' ', usandologica)
            usandologica.pop(-1)
            permiso = False
            return exp1 or exp2
        # si se muestran

        if Exp.operador == LOGICA.MAYORQUE :            
            x = ""
            
            x += crearIf(verboolastring(exp1) + ">" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)

            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  

            return True
        elif Exp.operador == LOGICA.MENORQUE :
            x = ""

            x += crearIf(verboolastring(exp1) + "<" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)
            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  

            return True
        elif Exp.operador == LOGICA.MAYORIWAL :
            x = ""

            x += crearIf(verboolastring(exp1) + ">=" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)

            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  

            return True
        elif Exp.operador == LOGICA.MENORIWAL : 
            x = ""
            x += crearIf(verboolastring(exp1) + "<=" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)

            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  

            return True
        elif Exp.operador == LOGICA.IWAL : 
            x = ""

            if comparandocadenas:
                if not yacomparestrings:
                    yacomparestrings = True
                    temp2 = crearTemporal()
                    temp3 = crearTemporal()
                    temp4 = crearTemporal()
                    temp5 = crearTemporal()
                    temp6 = crearTemporal()

                    salto1 = crearSalto()
                    salto2 = crearSalto()
                    salto3 = crearSalto()
                    salto4 = crearSalto()

                    y = ""
                    y += temp2 + siwal +getP("+1")
                    y += temp3 + siwal + getStack(temp2) + fincomando
                    y += tempmasmas(temp2)
                    y += temp4 + siwal + getStack(temp2) + fincomando
                    y += iniciarSalto(salto1)
                    y += temp5 +  siwal + getHeap(temp3) + fincomando
                    y += temp6 + siwal + getHeap(temp4) + fincomando
                    y += crearIf(temp5 + "!=" + temp6, salto3)
                    y += crearIf(temp5 + "== -1", salto2)
                    y += tempmasmas(temp3)
                    y += tempmasmas(temp4)
                    y += iniciarGoto(salto1)
                    y += iniciarSalto(salto2)
                    y += getStack("P") + siwal + "1" + fincomando #si alch son iwales
                    y += iniciarGoto(salto4)
                    y += iniciarSalto(salto3)
                    y += getStack("P") + siwal + "0" + fincomando #si alch no son iwales
                    y += iniciarSalto(salto4)
                    y += "return" + fincomando

                    meterfuncion('compareStrings', y)

                temp7 = crearTemporal()
                temp8 = crearTemporal()

                x += temp7 + siwal + getP("+" + str(contavars))
                x += tempmasmas(temp7)
                x += getStack(temp7) + siwal + exp1 + fincomando
                x += tempmasmas(temp7)
                x += getStack(temp7) + siwal + exp2 + fincomando
                x += aumentarP(contavars)
                x += "compareStrings()" + fincomando
                x += temp8 + siwal + getStack("P") + fincomando
                x += disminuirP(contavars)

                x += crearIf(temp8 + " == 1", saltotrue)
                x += iniciarGoto(saltofalse)
                meteraTraduccion(x)
                comparandocadenas = False
                return Exp.term1.id == Exp.term2.id
            
            x += crearIf(verboolastring(exp1) + "==" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)

            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  


            return exp1 == exp2
        elif Exp.operador == LOGICA.DISTINTO :
            x = ""
            
            if comparandocadenas:
                if not yacomparestrings:

                    temp2 = crearTemporal()
                    temp3 = crearTemporal()
                    temp4 = crearTemporal()
                    temp5 = crearTemporal()
                    temp6 = crearTemporal()

                    salto1 = crearSalto()
                    salto2 = crearSalto()
                    salto3 = crearSalto()
                    salto4 = crearSalto()

                    y = ""
                    y += temp2 + siwal +getP("+1")
                    y += temp3 + siwal + getStack(temp2) + fincomando
                    y += tempmasmas(temp2)
                    y += temp4 + siwal + getStack(temp2) + fincomando
                    y += iniciarSalto(salto1)
                    y += temp5 +  siwal + getHeap(temp3) + fincomando
                    y += temp6 + siwal + getHeap(temp4) + fincomando
                    y += crearIf(temp5 + "!=" + temp6, salto3)
                    y += crearIf(temp5 + "== -1", salto2)
                    y += tempmasmas(temp3)
                    y += tempmasmas(temp4)
                    y += iniciarGoto(salto1)
                    y += iniciarSalto(salto2)
                    y += getStack("P") + siwal + "1" + fincomando #si alch son iwales
                    y += iniciarGoto(salto4)
                    y += iniciarSalto(salto3)
                    y += getStack("P") + siwal + "0" + fincomando #si alch no son iwales
                    y += iniciarSalto(salto4)
                    y += "return" + fincomando

                    meterfuncion('compareStrings', y)

                temp7 = crearTemporal()
                temp8 = crearTemporal()

                x += temp7 + siwal + getP("+" + str(contavars))
                x += tempmasmas(temp7)
                x += getStack(temp7) + siwal + exp1 + fincomando
                x += tempmasmas(temp7)
                x += getStack(temp7) + siwal + exp2 + fincomando
                x += aumentarP(contavars)
                x += "compareStrings()" + fincomando
                x += temp8 + siwal + getStack("P") + fincomando
                x += disminuirP(contavars)

                x += crearIf(temp8 + " == 1", saltotrue)
                x += iniciarGoto(saltofalse)
                meteraTraduccion(x)
                comparandocadenas = False
                return Exp.term1.id == Exp.term2.id
            
            x += crearIf(verboolastring(exp1) + "!=" + verboolastring(exp2), saltotrue)
            x += iniciarGoto(saltofalse)
            meteraTraduccion(x)

            if "=0-" in str(exp1):
                u = exp1.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp1 = w
            if "=0-" in str(exp2):
                u = exp2.split("=0-")
                p = u[-1][:-1]
                p = p[:-1]
                w = -int(p)  
                exp2 = w  


            return exp1 != exp2
        else:  return ""
    elif isinstance(Exp, OPBool):
        if Exp.id == 'false':
            return False
        return True
    elif isinstance(Exp, OPNum):
        return Exp.val
    elif isinstance(Exp, OPCadena):
        temp, trad = stringaHeap(Exp.id)
        meteraTraduccion(trad)
        comparandocadenas = True
        return temp
    elif isinstance(Exp, LlamadaArr):
        print('Acá hay una llamada arr')
        print(Exp.nombre)
        print(Exp.inds)

        arr_indices = []
        contadimensiones = 0
        for indice in Exp.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if funcionusada != 0:
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(Exp.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        funcionusada = 4

        temp8 = crearTemporal()
        temp9 = crearTemporal()
        
        
        z = temp8 + siwal + getStack(str(arr.posicion)) + fincomando
        usandovars = usandovars +1
        meteraTraduccion(z) 
        
        try:
            if contadimensiones == 0: 
                checarIndice("-1", "0", "0")                
                return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                temp10 = crearTemporal()
                x = metercomentario("arr de una dimensión")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                x += temp10 + siwal + getHeap(temp9) + fincomando

                meteraTraduccion(x)
                funcionusada = 5
                return temp10
            elif contadimensiones == 2:
                temp10 = crearTemporal()
                temp11 = crearTemporal()
                temp12 = crearTemporal()

                x = metercomentario("arr de dos dimensiones")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                x += temp10 + siwal + getHeap(temp9) + fincomando

                
                x += checarIndice(verificarT(arr_indices[1]), temp10)
                x += temp11 + siwal + aumentartemp(temp10, verificarT(arr_indices[1]))
                x += tempmasmas(temp11)
                x += temp12 + siwal + getHeap(temp11) + fincomando

                meteraTraduccion(x)
                funcionusada = 5
                return temp12
            elif contadimensiones == 3: 
                temp10 = crearTemporal()
                temp11 = crearTemporal()
                temp12 = crearTemporal()
                temp13 = crearTemporal()
                temp14 = crearTemporal()

                x = metercomentario("arr de tres dimensiones")
                x += checarIndice(verificarT(arr_indices[0]), temp8)
                x += temp9 + siwal + aumentartemp(temp8, verificarT(arr_indices[0]))
                x += tempmasmas(temp9)
                x += temp10 + siwal + getHeap(temp9) + fincomando

                x += checarIndice(verificarT(arr_indices[1]), temp10)
                x += temp11 + siwal + aumentartemp(temp10, verificarT(arr_indices[1]))
                x += tempmasmas(temp11)
                x += temp12 + siwal + getHeap(temp11) + fincomando

                x += checarIndice(verificarT(arr_indices[2]), temp12)
                x += temp13 + siwal + aumentartemp(temp12, verificarT(arr_indices[2]))
                x += tempmasmas(temp13)
                x += temp14 + siwal + getHeap(temp13) + fincomando

                meteraTraduccion(x)
                funcionusada = 5
                return temp14
        except Exception as e:
            print(e)
            return errorEquis('Llamada a valor de arreglo', str(e))
    else: 
        print('viendo si se va a los numeros')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverNumerica(Exp, tablaSimbolos)

#endregion

# ------------------------------------------------------------------------- 
# AUXILIARES --------------------------------------------------------------
# ------------------------------------------------------------------------- 

# region Auxiliares
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

def tipoEnTabla(posicion, tablaSimbolos: cst.TablaSimbolos):
    return tablaSimbolos.obtenerTipo(posicion)

def borrardeTabla(simbolo: cst.NodoSimbolo):
    global lista_simbolos
    lista_simbolos.remove(simbolo)

def añadiraTabla(simbolo: cst.NodoSimbolo):
    global lista_simbolos
    lista_simbolos.append(simbolo)
 
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

# endregion

# ------------------------------------------------------------------------- 
# COMPILADOR --------------------------------------------------------------
# ------------------------------------------------------------------------- 

#region compilador
def funcionesencero():
    global yapotencia
    yapotencia = False
    global yaconcatstring
    yaconcatstring = False
    global yaprintstring
    yaprintstring = False
    global yalowercase
    yalowercase = False
    global yauppercase
    yauppercase = False
    global yagenerarArray 
    yagenerarArray = False
    global usandovars
    usandovars = 0
    global contavars
    contavars = 0
    global yacomparestrings 
    yacomparestrings = 0
    global inicioloop
    inicioloop = ""
    global findeloop
    findeloop = ""

def instruccionesencero():
    global usandovars
    usandovars = 0
    global usandologica
    usandologica = [2]
    global saltofalse
    saltofalse = ""
    global saltotrue 
    saltotrue = ""
    global saltorest
    saltorest = ""
    global comparandocadenas
    comparandocadenas = False
    

def meterPalabra(texto):
    aux = ""
    for i in texto:
        ascii = ord(i)
        aux += "fmt.Printf(\"%c\"," + str(ascii) +");\n"
    return aux

def metercomentario(texto):
    return "//" + texto + "\n"

# ARRAY
def checarIndice(indice, tempinicial):
    temp0 = crearTemporal()
    temp1 = crearTemporal()
    saltofalso = crearSalto()
    saltoverdadero = crearSalto()
    global ultimorest
    x = ""
    x += metercomentario("viendo indices de array")
    x += temp1 + siwal + getHeap(tempinicial) + fincomando
    x += temp0 + siwal + indice + fincomando
    x += crearIf(temp0 + " < 0", saltofalso)
    x += crearIf(temp0 + " > " + temp1, saltofalso)
    x += iniciarGoto(saltoverdadero)
    x += iniciarSalto(saltofalso)
    x += meterPalabra("BoundsError")
    x += iniciarGoto(ultimorest)
    x += iniciarSalto(saltoverdadero)
    x += metercomentario("fin de checar indices")
    return x

# BOOLS
def verboolastring(exp):
    var = verificarT(exp)
    if verificarT(exp) == False or 'alse' in verificarT(exp):
        var = "0"
    elif verificarT(exp) == True or 'rue' in verificarT(exp):
        var = "1"
    return var

# STRING
def stringaHeap(valor):
    posenH = crearTemporal()
    x = posenH + siwal + getH("")
            
    for i in valor:
        ascii = ord(i)
        x += getHeap("H") + siwal + str(ascii) + fincomando
        x += aumentarH(1)

    x += getHeap("H") + siwal + "-1" + fincomando
    x += aumentarH(1)
    return posenH, x

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

def metercomentario(texto):
    return "// " + texto + "\n" 

def checarLabelsNoUsadas(traduccion: str):
    global contasaltos
    global gotos

    for index in range(contasaltos):
        salto = "L" + str(index)
        goto = iniciarGoto(salto)
        goto2 = "{goto " + salto + "}\n"
        inicio = iniciarSalto(salto)

        x = traduccion.find(goto)
        y = traduccion.find(inicio)
        z = traduccion.find(goto2)
        if x == -1 and y != -1 and z == -1:
            traduccion = traduccion.replace(inicio, '')
            print('Salto eliminado: ', salto)

    return traduccion


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
    x = salto + ":\n"
    return x

def iniciarGoto(salto):
    global gotos
    x = "goto " + salto + ";\n"
    gotos.append(x)
    return x

# TEMPORALES
def crearTemporal():
    global contatemporales
    x = contatemporales
    contatemporales += 1
    return "t" + str(x)

def borrartemporal():
    global contatemporales
    contatemporales -= 1

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

def aumentartemp(temp: str, unidades:str):
    return temp + " + " + unidades + fincomando

def disminuirtemp(temp: str, unidades:int):
    return temp + " - " + str(unidades) + fincomando

# P 
def aumentarP(unidades: int):
    global p
    p = p + unidades
    trad = "P=P+" + str(unidades) + fincomando
    return trad

def disminuirP(unidades: int):
    global p
    p = p - unidades
    trad = "P=P-" + str(unidades) + fincomando
    return trad

def getP(mod):
    return "P" + mod + ";\n"

# H
def aumentarH(unidades: int):
    global h
    h = h + unidades
    trad = "H=H+" + str(unidades) + fincomando
    return trad

def disminuirH(unidades: int):
    global h
    h = h - unidades
    trad = "H=H-" + str(unidades) + fincomando
    return trad

def getH(mod):
    return "H" + mod + ";\n"

# HEAP
def getHeap(temporal):
    return "heap[int(" + str(temporal) + ")]"

# STACK
def getStack(temporal):
    return "stack[int(" + str(temporal) + ")]"

# endregion