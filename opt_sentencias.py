
class Instruccion:
    '''This is an abstract class'''

#TODAS LAS CLASES TIENEN UN txt, que es literal el texto de la instruccion

class InicioSalto(Instruccion): 
    def __init__(self,  salto, txt) :
        self.salto = salto
        self.txt = txt

class InicioGoto(Instruccion): 
    def __init__(self,  salto, txt) :
        self.salto = salto
        self.txt = txt

class InicioIf(Instruccion): 
    def __init__(self, comparacion, salto, txt) :
        self.comparacion = comparacion
        self.salto = salto
        self.txt = txt

class Asignacion(Instruccion): # izq, der
    def __init__(self,  izquierda, derecha, txt) :
        self.izquierda = izquierda
        self.derecha = derecha
        self.txt = txt

class Impresion(Instruccion): 
    def __init__(self,  tipo, char, txt) :
        self.tipo = tipo
        self.char = char
        self.txt  = txt

class LlamadaMetodo(Instruccion): 
    def __init__(self,  metodo, txt) :
        self.metodo = metodo
        self.txt = txt

class Metodo(Instruccion): 
    lista = []
    def __init__(self,  metodo, lista) :
        self.metodo = metodo
        self.lista = lista


# otros

class Comparacion(Instruccion): # izq, simbolo, der
    def __init__(self,  izquierda, simbolo, derecha, txt) :
        self.izquierda = izquierda
        self.simbolo = simbolo
        self.derecha = derecha
        self.txt = txt