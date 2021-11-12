# importo todo de todos lados
from sys import exc_info, getsizeof
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 
import re

import optimizador
#from optimizador.opt_lexico import fighting, tokens
from optimizador.opt_sintactico import opt_sintactico

import math
import opt_sentencias as sent


exporte = cst.Exporte('', [], [], [], [])
textofinal = ""
textoInicial = ""
nuevasInstrucciones = []
reporteOptimizacion = []
cadenaOptimizada = ""
asignacionesPrevias = []
nombreMetodo = ""

#agarro el texto de la entrada, quito headers, lo paso por el sintáctico, 
# lo paso por la optimizaión (que regresa un texto) y lo retorno
def optimizar(texto: str):

    global reporteOptimizacion
    global nuevasInstrucciones
    global exporte
    global textofinal 
    global cadenaOptimizada
    global asignacionesPrevias
    global nombreMetodo
    global ultimaAsignacion
    global textoInicial

    textoOptimizado = ""

    reporteOptimizacion = [cst.Optimizacion("prueba", "0", "0", "0", "-1")]
    nuevasInstrucciones = []

    headers = """package main\nimport ("fmt")\n"""
    headers += "var stack [300000]float64\nvar heap [300000]float64\n"
    headers += "var P, H float64\n"

    texto = re.sub(r'^.*?\n', '', texto)
    texto = re.sub(r'^.*?\n', '', texto)
    texto = re.sub(r'^.*?\n', '', texto)
    texto = re.sub(r'^.*?\n', '', texto)
    texto = re.sub(r'^.*?\n', '', texto)

    headers += texto.split("float64", 1)[0]
    headers += "float64\n\n"
    texto = re.sub(r'^.*?\n', '', texto)

    textoInicial = texto
    listametodos = optimizador.opt_sintactico(texto)
    textoOptimizado = iniciarOptimizacion(listametodos)

    exporte = cst.Exporte('', [], [], [], [])
    exporte.reporteOptimizacion = reporteOptimizacion
    exporte.traduccion = "// texto optimizado por Optimizador 1\n" + headers + textoOptimizado  
    return exporte
    
# agarro la lista de métodos que regresa el sintáctico, lo optimizo
#lo convierto en cadena y lo regreso
def iniciarOptimizacion(listametodos):
    global reporteOptimizacion
    global nuevasInstrucciones
    global exporte
    global textofinal 
    global cadenaOptimizada
    global asignacionesPrevias
    global nombreMetodo

    cadenaAuxiliar = ""
    cadenaOptimizada = ""
    cadenafinal = ""
    contador = 0

    print('LISTA; ', listametodos)

    for metodo in listametodos:  
        if isinstance(metodo, sent.Metodo):
            print('METODO ', contador)
            cadenaAuxiliar = ""
                
            cadenaAuxiliar += "func " + metodo.metodo + "() {\n" #metiendo el método a la cadena final
            nombreMetodo = metodo.metodo

            nuevasInstrucciones = []
            nuevasInstrucciones1 = reglas2_3(metodo.lista)
            nuevasInstrucciones2 = reglas6_7_8(nuevasInstrucciones1)
            nuevasInstrucciones3 = regla5(nuevasInstrucciones2)
            nuevasInstrucciones4 = reglas4_5(nuevasInstrucciones3)
            # acá meto las reglas por las que pasan los cositos
            nuevasInstrucciones = nuevasInstrucciones4
            for instruccion in nuevasInstrucciones:
                try:
                    cadenaAuxiliar += instruccion.txt + "\n"
                except Exception as ee:
                    print('Asignación', 'algo x pasó :c' + ee)

            cadenaAuxiliar += "return;\n}\n" #cerrando el método
            #print(cadenaAuxiliar)
            #cadenaOptimizada += cadenaAuxiliar
            cadenafinal += cadenaAuxiliar
            cadenaAuxiliar = ""
      
    return cadenafinal

def reglas4_5(instrucciones = []):
    global reporteOptimizacion

    print('REGLA 4_5')
    contador = 0
    for miinstruccion in instrucciones:

        inicial = miinstruccion.txt
        if isinstance(miinstruccion, sent.InicioGoto):
            print('GOTO YA')
            indexSalto = 0
            encontrado = False
            for buscandoSalto in instrucciones:
                if isinstance(buscandoSalto, sent.InicioSalto):
                    # viendo si el salto coincide con el goto
                    #print(miinstruccion.salto, " , ", buscandoSalto.salto)
                    if miinstruccion.salto == buscandoSalto.salto:
                        #print('REGLA 4 1/2 -- index: ', indexSalto)
                        encontrado = True
                        break
                
                indexSalto += 1

            if isinstance(instrucciones[indexSalto +1], sent.InicioGoto) and encontrado:
                #print('REGLA 4 2/2')
                instrucciones[contador] = instrucciones[indexSalto +1]
                regla = "4"
                reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, instrucciones[contador].txt, str(contador)))         

        elif isinstance(miinstruccion, sent.InicioIf):
            print('IF YA')
            indexSalto = 0
            encontrado = False
            for buscandoSalto in instrucciones:
                if isinstance(buscandoSalto, sent.InicioSalto):
                    # viendo si el salto coincide con el goto
                    #print(miinstruccion.salto, " , ", buscandoSalto.salto, "???")
                    if miinstruccion.salto == buscandoSalto.salto:
                        print('REGLA 4 1/2 -- index: ', indexSalto)
                        encontrado = True
                        break
                
                indexSalto += 1

            if isinstance(instrucciones[indexSalto +1], sent.InicioGoto) and encontrado:
                print('REGLA 4 2/2')
                instrucciones[contador].txt = "if(" + miinstruccion.comparacion.txt + ") {" + instrucciones[indexSalto +1].txt + "}"
                regla = "5"
                reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, instrucciones[contador].txt, str(contador)))         


        contador += 1
    
    return instrucciones


def regla5(instrucciones = []):
    global reporteOptimizacion
    global asignacionesPrevias

    print('REGLA 1')
    contador = 0
    nuevasinstrucciones = instrucciones
    print('al inicio', nuevasInstrucciones)
    print('comparado con', instrucciones)

    for miinstruccion in instrucciones:

        inicial = miinstruccion.txt
        if isinstance(miinstruccion, sent.Asignacion):
            print('ASIGNACION')
            regla = "1"
            print('previas', len(asignacionesPrevias))
            for asignacion in asignacionesPrevias:
                if asignacion.derecha == miinstruccion.izquierda and asignacion.izquierda == miinstruccion.derecha:
                    print('MATCH PARA ELIMINAR')
                    instrucciones[contador] = sent.Eliminado("")
                    reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
                    contador += 1
                    continue

            asignacionesPrevias.append(miinstruccion)
        elif isinstance(miinstruccion, sent.InicioSalto):
            asignacionesPrevias = []

        contador += 1

    return instrucciones      


# recibe una lista, mira las instrucciones, devuelve una lista
def reglas6_7_8(instrucciones = []):
    global reporteOptimizacion

    print('REGLAS 6-9')
    contador = 0
    nuevasinstrucciones = instrucciones

    for miinstruccion in instrucciones:

        inicial = miinstruccion.txt
        if isinstance(miinstruccion, sent.Asignacion):
            #print('ASIGNACION')
            #print(miinstruccion.izquierda)
            #print(miinstruccion.derecha)
            regla = "6"
            if miinstruccion.izquierda in miinstruccion.derecha:
                #si se asigna a si mismo

                aux = miinstruccion.derecha
                if "+" in aux:
                    arr = aux.split("+")
                    if arr[0] == "0" or arr[1] == "0":
                        # suma con 0
                        nuevasinstrucciones[contador] = sent.Eliminado("")
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
                elif "-" in aux:
                    arr = aux.split("-")
                    if arr[1] == "0":
                        # resta con 0
                        nuevasinstrucciones[contador] = sent.Eliminado("")
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
                elif "*" in aux:
                    arr = aux.split("*")
                    if arr[0] == "1" or arr[1] == "1":
                        # mult con 1
                        nuevasinstrucciones[contador] = sent.Eliminado("")
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
                    elif arr[0] == "0" or arr[1] == "0":
                        # mult con 0
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=0;"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, "0", nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif arr[0] == "2":
                        # mult con 2
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=" + arr[1] + "+" + arr[1]  +";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[1] + "+" + arr[1] , nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif arr[1] == "2":
                        # mult con 2
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=" + arr[0] + "+" + arr[0]  +";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0] + "+" + arr[0] , nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                elif "/" in aux:
                    arr = aux.split("/") 
                    if arr[1] == "1":
                        # div sobre 1
                        nuevasinstrucciones[contador] = sent.Eliminado("")
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))     
                    elif arr[0] == "0":
                        # mult con 0
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=0;"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, "0", nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))         
            else:
                #si no se asigna a si mismo
                regla = "7"
                aux = miinstruccion.derecha
                if "+" in aux:
                    arr = aux.split("+")
                    if arr[0] == "0": # 0 + algo
                        nueva = miinstruccion.izquierda + "=" + arr[1] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[1], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif  arr[1] == "0": # algo + 0
                        nueva = miinstruccion.izquierda + "=" + arr[0] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                elif "-" in aux:
                    arr = aux.split("-")
                    if arr[1] == "0":
                        nueva = miinstruccion.izquierda + "=" + arr[0] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                elif "*" in aux:
                    arr = aux.split("*")
                    if arr[0] == "1": # 1* algo
                        nueva = miinstruccion.izquierda + "=" + arr[1] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[1], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif  arr[1] == "1": # algo *1
                        nueva = miinstruccion.izquierda + "=" + arr[0] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif arr[0] == "0" or arr[1] == "0":
                        # mult con 0
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=0;"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, "0", nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif arr[0] == "2":
                        # mult con 2
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=" + arr[1] + "+" + arr[1]  +";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[1] + "+" + arr[1] , nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                    elif arr[1] == "2":
                        # mult con 2
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=" + arr[0] + "+" + arr[0]  +";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0] + "+" + arr[0] , nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))
                elif "/" in aux:
                    arr = aux.split("/") 
                    if arr[1] == "1":
                        nueva = miinstruccion.izquierda + "=" + arr[0] + ";"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, arr[0], nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))  
                    elif arr[0] == "0":
                        # mult con 0
                        regla = "8"
                        nueva = miinstruccion.izquierda + "=0;"
                        nuevasinstrucciones[contador] = sent.Asignacion(miinstruccion.izquierda, "0", nueva)
                        reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nueva, str(contador)))             
            

        contador += 1

    return nuevasinstrucciones

def reglas2_3( instrucciones = []):
    global reporteOptimizacion
    global textoInicial

    print('REGLAS 2-3')
    contador = 0
    nuevasinstrucciones = instrucciones
    #print('nuevasinstrucciones ', nuevasinstrucciones)

    regla1Abierta = False
    eliminarAbierto1 = False
    eliminarAbierto2 = False

    for miinstruccion in instrucciones:
        inicial = miinstruccion.txt

        #print('voy por la instruccion ', contador)
        if regla1Abierta:
            if isinstance(miinstruccion, sent.InicioSalto):
                regla1Abierta = False
                print('REGLA 1 CANCELADA')
                nuevasinstrucciones[contador].txt = miinstruccion.txt
            else:
                regla = "2"
                anterior = miinstruccion.txt
                nuevasinstrucciones[contador] = sent.Eliminado("")
                reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
        else:
            if eliminarAbierto2:
                if isinstance(miinstruccion, sent.InicioSalto):
                    print('Salto para eliminar')
                    eliminarAbierto2 = False #acá es cuado ya eliminé el iniciogoto
                    regla = "3"
                    nuevasinstrucciones[contador] = sent.Eliminado("")
                    reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))


        if isinstance(miinstruccion, sent.InicioGoto) and not regla1Abierta:
            if not eliminarAbierto1:
                regla1Abierta = True
                print('REGLA 1 INICIADA')
                nuevasinstrucciones[contador].txt = miinstruccion.txt                
            else:
                print('Salto para eliminar')
                eliminarAbierto1 = False
                regla = "3"
                nuevasinstrucciones[contador] = sent.Eliminado("")
                reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))

        # REGLA 3
        elif isinstance(miinstruccion, sent.InicioIf) and len(instrucciones) > (contador +2):
            print('REGLA 3 1/3')
            if isinstance(instrucciones[contador +1], sent.InicioGoto) and isinstance(instrucciones[contador +2], sent.InicioSalto):
                # si el orden es if, goto, iniciosalto 
                gotoaux = instrucciones[contador +1]     
                print('REGLA 3 2/3')       
                if str(miinstruccion.salto) in  instrucciones[contador + 2].txt and isinstance(miinstruccion.comparacion, sent.Comparacion):
                    # si el salto del if es al iniciosalto en dos cositos                    
                    print('REGLA 3 3/3')
                    gotoOriginal = miinstruccion.salto                    
                    arrtemp = instrucciones[contador +3:]
                    sigo = False
                    contasalto = 0
                    for instemp in arrtemp:
                        if isinstance(instemp, sent.InicioSalto): 
                            if instemp.salto in gotoaux.txt:
                                sigo = True
                                break
                            else:
                                break
                    
                    filtrofinal = textoInicial.count(gotoOriginal)
                    print('gotoOriginal ', gotoOriginal, ' está: ', filtrofinal, ' veces')
                    if filtrofinal > 2:
                        sigo = False
                        print('REGLA 3 NO APLICA')

                    if not sigo:
                        print('REGLA 3 CANCELADA')
                        nuevasinstrucciones[contador].txt = miinstruccion.txt
                        contador += 1
                        continue

                    print('REGLA 3 4/3')

                    micomparacion = miinstruccion.comparacion
                    if micomparacion.simbolo == "<":
                        micomparacion.simbolo = ">"
                    elif micomparacion.simbolo == ">":
                        micomparacion.simbolo = "<"
                    elif micomparacion.simbolo == ">=":
                        micomparacion.simbolo = "<="
                    elif micomparacion.simbolo == "<=":
                        micomparacion.simbolo = ">="
                    elif micomparacion.simbolo == "==":
                        micomparacion.simbolo = "!="
                    elif micomparacion.simbolo == "!=":
                        micomparacion.simbolo = "=="

                    miinstruccion.comparacion = micomparacion
                    micomparacion.txt = micomparacion.izquierda + micomparacion.simbolo + micomparacion.derecha
                    miinstruccion.comparacion.txt = micomparacion.txt

                    nuevasinstrucciones[contador].txt = "if (" + micomparacion.txt + "){" + gotoaux.txt + "}\n"
                    regla = "3"
                    reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, nuevasinstrucciones[contador].txt, str(contador)))
                    eliminarAbierto1 = True
                    eliminarAbierto2 = True
            
        contador += 1
    return nuevasinstrucciones




