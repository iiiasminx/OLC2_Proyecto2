from datetime import datetime

# ----------------------------------- OBJ EXPORTACION ------------------------------
#-----------------------------------------------------------------------------------

class Exporte:
    listasemanticos = []
    listasegundos = []
    def __init__(self, traduccion, tabla_simbolos, tabla_errores, errores_lexicos, arbol):
        self.traduccion = traduccion
        self.tabla_simbolos = tabla_simbolos
        self.tabla_errores = tabla_errores
        self.errores_lexicos = errores_lexicos
        self.arbol = arbol

# ------------------------------------- TABLA ERRORES -----------------------------
#-----------------------------------------------------------------------------------
class NodoError:

    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y %H:%M:%S")
    def __init__(self, contador, descripcion, fila, columna):
        self.contador = contador
        self.fila = fila
        self.columna = columna
        self.descripcion = descripcion

class NodoErrorSemantico:

    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y %H:%M:%S")
    fila = 'nc'
    columna = 'nc'
    contador = 0
    def __init__(self, descripcion):
        self.descripcion = descripcion


# ------------------------------ TABLA DE SÍMBOLOS ---------------------------------
#-----------------------------------------------------------------------------------
class NodoSimbolo:
    nota = ''
    fila = 'nc'
    columna = 'nc'
    funcinstrucciones = []
    funcparams = []
    def __init__(self, nombre, tipo, ambito, posicion):
        self.nombre = nombre    # juanito, eve, shion
        self.tipo = tipo        # int, funcion, bool, etc
        self.ambito = ambito    #global, local
        #self.valor = valor      #45, 55, "wakateru" 
        self.posicion = posicion #1,2,3 .. va en orden


class TablaSimbolos:

    simbolos = {

        "prueba": NodoSimbolo('prueba', 'prueba', 'global', 'prueba')
    }
    def __init__(self) : #el init recibe un obejto de símbolos (?)
        pass        # se lo cambié a un array xd

    def agregar(self, simbolo: NodoSimbolo) :
        self.simbolos[simbolo.nombre] = simbolo

    def obtener(self, nombre) : #aca miro si existe o no el coso
        if not nombre in self.simbolos :
            desc = "Error semántico - no se encuentra la variable: " + str(nombre)
            error1 = NodoErrorSemantico(desc)
            return error1
        return self.simbolos[nombre]

    def actualizar(self, simbolo) :
        if not simbolo.nombre in self.simbolos :
            desc = 'Error semántico - no se encuentra la variable: ' + str(simbolo.nombre)
            error1 = NodoErrorSemantico(desc)
            return error1
        else :
            self.simbolos[simbolo.nombre] = simbolo
   
