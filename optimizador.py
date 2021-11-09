# importo todo de todos lados
from sys import exc_info, getsizeof
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 

from opt_lexico import fighting, tokens
import math

class Optimizador1:

    exporte = cst.Exporte('', [], [], [], [])

    def optimizar(self, texto: str):

        texto = texto.replace("package main\nimport (\"fmt\")\n", "")
        texto = texto.replace("var stack [300000]float64\nvar heap [300000]float64\n", "")
        texto = texto.replace("var P, H float64\n", "")

        headers = """package main\nimport ("fmt")\n"""
        headers += "var stack [300000]float64\nvar heap [300000]float64\n"
        headers += "var P, H float64\n"
        headers += texto[:texto.find('\n')] # estas son las variables

        texto = texto[texto.find('\n'):] # ya tengo el texto sin headers
        fighting(texto)

        self.exporte.traduccion = "// texto optimizado por Optimizador 1\n" + texto  
        return self.exporte


class Optimizador2:

    exporte = cst.Exporte('', [], [], [], [])

    def optimizar(self, texto):

        self.exporte.traduccion = '//texto optimizado por Optimizador 2\n' + texto 
        return self.exporte