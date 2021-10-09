from enum import Enum

class ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    ASTERISCO = 3
    DIVIDIDO = 4
    MODULO = 5
    ELEVADO = 6

class MATH(Enum):
    LOG10 = 1
    SIN = 2
    COS = 3
    TAN = 4
    SQRT = 5

class LOGICA(Enum) :
    AND = 1
    OR = 2
    MAYORQUE = 3
    MENORQUE = 4
    MAYORIWAL = 5
    MENORIWAL = 6
    IWAL = 7
    DISTINTO = 8

# Numeros -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class Expnum:
    pass


class OPBinaria(Expnum) :
    def __init__(self, term1, operador, term2) :
        self.term1 = term1
        self.term2 = term2
        self.operador = operador

class OPNeg(Expnum) :

    def __init__(self, term) :
        self.term = term

class OPNativa(Expnum) : #log10, sin, cos, tan, sqrt

    def __init__(self, term, tipo) :
        self.term = term
        self.tipo = tipo

class OPNativaLog(Expnum) : 

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPArray(Expnum) :

    def __init__(self, val = []) :
        self.val = val

class OPNum(Expnum) :

    def __init__(self, val = 0) :
        self.val = val

# Cadenas -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class ExpCadena:
    pass

class OPMergeString(ExpCadena) :

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPElevarString(ExpCadena) :

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPUppercase(ExpCadena) :

    def __init__(self, term1) :
        self.term1 = term1

class OPLowercase(ExpCadena) :

    def __init__(self, term1) :
        self.term1 = term1

class OPLength(ExpCadena) : #este está tentativo acá

    def __init__(self, term1) :
        self.term1 = term1


class OPPush:
    nombre = ""
    def __init__(self, arreglo, term) :
        self.arreglo = arreglo
        self.term = term

class OPPop:
    nombre =""
    def __init__(self, arreglo) :
        self.arreglo = arreglo

class OPCadena(ExpCadena) :

    def __init__(self, id = "") :
        self.id = id


# Bool ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class ExpBool:
    pass

class OPPASS:
    def __init__(self, id = "") :
        self.id = id

class OPBool(ExpBool) : #si viene un id, de qué hereda? :c

    def __init__(self, id = True) :
        self.id = id


class OPLogica() :
    def __init__(self, term1, operador, term2) :
        self.term1 = term1
        self.term2 = term2
        self.operador = operador


# Otros ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


class OPID(Expnum) : #id

    def __init__(self, id = "") :
        self.id = id


#OTROSSSS

class OPNothing() : #no viene nada

    def __init__(self, id = "") :
        self.id = id

class OPType() : #id

    def __init__(self, id ) :
        self.id = id


# Arreglos ------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

#lado izq del iwal
class LlamadaArr():
    def __init__(self, nombre, inds) :
        self.nombre = nombre
        self.inds = inds

class OPIndArr():
    def __init__(self, id = 0) :
        self.id = id

class OPIndArrs():
    def __init__(self, *ids) :
        self.ids = ids

#lado derecho del iwal
class Arrcont():
    def __init__(self, array) :
        self.array = array

# Structs -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class OPAtributpTipado(Expnum) : 

    def __init__(self, id, tipo) :
        self.id = id
        self.tipo = tipo

class OPAtributo(Expnum) :

    def __init__(self, id = "") :
        self.id = id


class OPTransferencia: #1 = break, #2 = continue, #3, return
    def __init__(self, tipo, obj = "") :
        self.tipo = tipo
        self.obj = obj


class ParamF:
    def __init__(self, id, tipo = "") :
        self.id = id
        self.tipo = tipo