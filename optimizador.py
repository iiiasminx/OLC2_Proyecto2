# importo todo de todos lados
from sys import exc_info, getsizeof
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 
import re

from opt_lexico import fighting, tokens
import math
import opt_sentencias as sent
from opt_sintactico import opt_sintactico

exporte = cst.Exporte('', [], [], [], [])
textofinal = ""
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

    listametodos = opt_sintactico(texto)
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
            # acá meto las reglas por las que pasan los cositos
            nuevasInstrucciones = nuevasInstrucciones1
            for instruccion in nuevasInstrucciones:
                try:
                    cadenaAuxiliar += instruccion.txt + "\n"
                except Exception as ee:
                    print('Asignación', 'algo x pasó :c' + ee)

            cadenaAuxiliar += "}\n" #cerrando el método
            #print(cadenaAuxiliar)
            #cadenaOptimizada += cadenaAuxiliar
            cadenafinal += cadenaAuxiliar
            cadenaAuxiliar = ""
      
    return cadenafinal

# recibe una lista, mira las instrucciones, devuelve una lista
def reglas2_3( instrucciones = []):
    global reporteOptimizacion
    global nuevasInstrucciones
    global exporte
    global textofinal 
    global cadenaOptimizada
    global asignacionesPrevias
    global nombreMetodo

    print('REGLAS 2-3')
    contador = 0
    nuevasinstrucciones = instrucciones
    #print('nuevasinstrucciones ', nuevasinstrucciones)

    regla1Abierta = False
    eliminarAbierto1 = False
    eliminarAbierto2 = False

    for miinstruccion in instrucciones:
        inicial = miinstruccion.txt

        print('voy por la instruccion ', contador)
        if regla1Abierta:
            if isinstance(miinstruccion, sent.InicioSalto):
                regla1Abierta = False
                print('REGLA 1 CANCELADA')
                nuevasinstrucciones[contador].txt = miinstruccion.txt
            else:
                regla = "2"
                anterior = miinstruccion.txt
                nuevasinstrucciones[contador].txt = ""
                reporteOptimizacion.append(cst.Optimizacion("Mirilla", regla, inicial, "cadena eliminada", str(contador)))
        else:
            if eliminarAbierto2:
                if isinstance(miinstruccion, sent.InicioSalto):
                    print('Salto para eliminar')
                    eliminarAbierto2 = False #acá es cuado ya eliminé el iniciogoto
                    regla = "3"
                    nuevasinstrucciones[contador].txt = ""
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
                nuevasinstrucciones[contador].txt = ""
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
                    arrtemp = instrucciones[contador +3:]
                    sigo = False
                    for instemp in arrtemp:
                        if isinstance(instemp, sent.InicioSalto): 
                            if instemp.salto in gotoaux.txt:
                                sigo = True
                                break
                            else:
                                break

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




