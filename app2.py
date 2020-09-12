from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__) 

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
        if producto == "" or precio == "" or precio <= 0:
            return "Formato no valido"
        else:
            print(producto)
            print(precio)
            return "Recibido"


@app.route("/successful")
def successful():
    return render_template("successful.html")


if __name__ == '__main__': 
    app.run(debug=True)