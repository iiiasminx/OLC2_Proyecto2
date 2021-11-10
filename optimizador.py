# importo todo de todos lados
from sys import exc_info, getsizeof
import objetos as cst
from operaciones import *
from instrucciones  import *
from a_sintactico import * 
import re

from opt_lexico import fighting, tokens
import math

from opt_sintactico import opt_sintactico

class Optimizador1:

    exporte = cst.Exporte('', [], [], [], [])
    textofinal = ""
    nuevasInstrucciones = []
    reporteOptimizacion = []
    cadenaOptimizada = ""
    asignacionesPrevias = []

    def optimizar(self, texto: str):

        headers = """package main\nimport ("fmt")\n"""
        headers += "var stack [300000]float64\nvar heap [300000]float64\n"
        headers += "var P, H float64\n"

        texto = re.sub(r'^.*?\n', '', texto)
        texto = re.sub(r'^.*?\n', '', texto)
        texto = re.sub(r'^.*?\n', '', texto)
        texto = re.sub(r'^.*?\n', '', texto)
        texto = re.sub(r'^.*?\n', '', texto)

        headers += texto.split("\n", 1)[0]
        texto = re.sub(r'^.*?\n', '', texto)

        listametodos = opt_sintactico(texto)
        textoOptimizado = self.iniciarOptimizacion(listametodos)

        self.exporte.traduccion = "// texto optimizado por Optimizador 1\n" + headers + textoOptimizado  
        return self.exporte
    
    def iniciarOptimizacion(self, listametodos):
        
        return self.cadenaOptimizada

    def regla1(instrucciones = []):
        contador = 0
        reglaAbierta = False
        eliminarAbierto = False

        for instruccion in instrucciones:

            if reglaAbierta:
                pass

            


class Optimizador2:

    exporte = cst.Exporte('', [], [], [], [])

    def optimizar(self, texto):

        self.exporte.traduccion = '//texto optimizado por Optimizador 2\n' + texto 
        return self.exporte