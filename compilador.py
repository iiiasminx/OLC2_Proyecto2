# importo todo de todos lados
from sys import exc_info
from a_lexico import fighting, tokens
import objetos as cst
from operaciones import *
from semantico  import *
from a_sintactico import * 
import math

traduccion = ""


def compilando(texto):
    print('Esto es lo que tengo que traducir', texto)
    global traduccion  
    traduccion = """package main\nimport ("fmt")\n"""
    traduccion += "var stack [10000]float64\nvar heap [100000]float64\n"
    traduccion += "var P, H float64\n\n"

    # probando lexico
    lexicos = fighting(texto)

    #probando sintactico
    paquete = fighting2(texto)

    #metiendo encabezados
    
    traduccion += "func main() {\n"
    traduccion += "codigo traducido"
    traduccion += "\n}"  

    paquete.traduccion = traduccion  
    paquete.errores_lexicos =lexicos

    return paquete




