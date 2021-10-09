from datetime import datetime

# ----------------------------------- OBJ EXPORTACION ------------------------------
#-----------------------------------------------------------------------------------

class Exporte:
    listasemanticos = []
    listasegundos = []
    def __init__(self, interpretacion, tabla_simbolos, grafo, tabla_errores, arbol):
        self.interpretacion = interpretacion
        self.tabla_simbolos = tabla_simbolos
        self.grafo = grafo
        self.tabla_errores = tabla_errores
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

# ------------------------------------- AST ------------------------------------
#-----------------------------------------------------------------------------------

class GrafoCST:    

    pilahijos = []  #pila de arrays de nodos [[],[],[],[]] lista de listas if u may

    #declaración de nodos
    textoNodo = ""
    pilaNodos = []

    #declaración de relaciones de unos a otros
    pilaLimites = []
    textoEdges = ""

    contador = 0
    texto = []

    #Genera los padres en funcion de los ultimos datos en la pila de Hijos
    #la posición es la posición de la producción en la que está
    #ej UNO : cadena DOS
    #generarpadre(2)
    def generarPadre(self, posicion):
        posicion -= 1
        limites = self.pilahijos.pop()
        
        for temp in limites:
            dictaux = {
                "from" : self.contador + posicion,
                "to" : temp["id"]
            }
            self.pilaLimites.append(dictaux)
            strxx = str(self.contador+posicion) + " -> " + str(temp["id"]) + "\n"
            self.textoEdges += strxx


    #genera los hijos del cosito, solo recibe strings
    def generarHijos(self, *listahijos ): #este es cuando genera solo strings (?)

        hijos = []

        for elemento in listahijos:
            hijo = {
                "id" : self.contador,
                "label": elemento #str(elemento)
            }
            hijos.append(hijo)              #lista de hijos del padre
            self.pilaNodos.append(hijo)     #lista de hijos general -- ESTO ME SIRVE PARA EL INTÉRPRETE

            auc = str(elemento).replace('"', '\'')

            straux = str(self.contador) + "[label= \"" + auc +"\"]\n"
            self.textoNodo += straux
            self.contador += 1
        
        self.pilahijos.append(hijos) #pila de arrays de nodos [[],[],[],[]] lista de listas if u may

    def generarTexto(self, txt):
        self.texto.append[txt]



# ------------------------------ TABLA DE SÍMBOLOS ---------------------------------
#-----------------------------------------------------------------------------------
class NodoSimbolo:
    nota = ''
    fila = 'nc'
    columna = 'nc'
    funcinstrucciones = []
    funcparams = []
    def __init__(self, nombre, tipo, ambito, valor):
        self.nombre = nombre
        self.tipo = tipo        # int (?)
        self.ambito = ambito    #global
        self.valor = valor


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
   
