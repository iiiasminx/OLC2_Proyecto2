from flask import Flask, render_template, request, jsonify
import json

from a_lexico import fighting
from a_sintactico import fighting2
from compilador  import compilando
from optimizador import optimizar
#from interprete import fightingfinal

app = Flask(__name__, static_url_path='')

# FUNCIONES EXTRA
def compilado(codigo):

    paquete = compilando(codigo)
    print('errores:')
    for x in range(len(paquete.tabla_errores)):
        print(paquete.tabla_errores[x].descripcion)
    #ahora si viendo que pex
    return paquete


def optim1(codigo):
    optimizado = optimizar(codigo)
    return optimizado

def optim2(codigo):
    optimizador1 = Optimizador2()
    optimizado = optimizador1.optimizar(codigo)
    txt = optimizado
    return txt


# FUNCIONES DE APP
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        entrada = request.form['entrada']
        print('Este es ->' + entrada)

        if 'Compilar' in request.form:
            paquete = compilado(entrada)
        elif 'Optimizar1' in request.form:
            paquete = optim1(entrada)
        elif 'Optimizar2' in request.form:
            paquete = optim2(entrada)

        return render_template('index.html', salida=paquete.traduccion, entrada=entrada, 
        errores=paquete.tabla_errores, lexicos=paquete.errores_lexicos, 
        simbolos=paquete.tabla_simbolos, semanticos= paquete.listasemanticos, optimizacion= paquete.reporteOptimizacion)

@app.route('/submit', methods=['GET'])
def submit2():
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()




