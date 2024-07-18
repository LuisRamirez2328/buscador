from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import re

app = Flask(__name__)

datos = pd.read_excel("libros.xlsx")

def validar_contraseña(password):
    if len(password) < 8 or len(password) > 15:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if re.search(r"\s", password):
        return False
    if not re.search("[!@#$%^&*()]", password):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if validar_contraseña(password):
            return redirect(url_for('index'))
        else:
            error_message = "La contraseña no cumple con los criterios de validación."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

def search_nombre(patron):
    datos[['Clave', 'Nombre', 'Correo', 'Telefono']] = datos[['Clave', 'Nombre', 'Correo', 'Telefono']].fillna('')
    coincidence = datos[datos['Nombre'].str.contains(patron, case=False, na=False) | datos['Correo'].str.contains(patron, case=False, na=False)]
    return coincidence[['Clave', 'Nombre', 'Correo', 'Telefono']]

@app.route('/buscador')
def index():
    return render_template('Formulario.html')

@app.route('/Lista', methods=['POST'])
def lista():
    searchnombres = request.form['nombre']
    result = search_nombre(searchnombres)
    if not result.empty:
        resultados = result.to_dict(orient='records')
        return render_template('resultado.html', resultados=resultados)
    else:
        return render_template('resultado.html')

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/new-endpoint')
def new_endpoint():
    return "This is a new endpoint!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
