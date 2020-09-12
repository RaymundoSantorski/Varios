from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'

@app.route("/") 
def index(): 
    return render_template("index.html")

@app.route("/productos")
def product():
    return render_template("producto.html")

@app.route("/carrito", methods = ['POST'])
def carrito():
    if request.method == 'POST':
        producto = request.form['producto']
        precio = request.form['precio']
        precioFormat = int(precio)
        if producto == "" or precio == "" or precioFormat <= 0:
            return "Formato no valido"
        else:
            flash('Producto agregado satisfactoriamente')
            return redirect(url_for('index'))


@app.route("/successful")
def successful():
    return render_template("successful.html")


if __name__ == '__main__': 
    app.run(debug=True)