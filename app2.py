from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os


app = Flask(__name__)

#conección a sqlite3

# settings
app.secret_key = 'mysecretkey'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'static/')

@app.route("/") 
def index(): 
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM Productos')
    data = cur.fetchall()
    return render_template("index.html", productos = data)

@app.route("/productos")
def product():
    return render_template("producto.html")

@app.route("/carrito", methods = ['POST'])
def carrito():
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("couldnt create upload directory: {}".format(target))
    if request.method == 'POST':
        producto = request.form['producto']
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        precioFormat = int(precio)
        filename = imagen.filename
        destination = "/".join([target, filename])
        if producto == "" or precio == "" or precioFormat <= 0:
            return "Formato no valido"
        else:
            imagen.save(destination)
            con = sqlite3.connect('mydb.db')
            cur = con.cursor()
            cur.execute('INSERT INTO Productos (Producto, Imagen, Descripcion, Precio) VALUES (?,?,?,?)',(producto, filename, descripcion, precio))
            con.commit()
            flash('Producto agregado satisfactoriamente')
            return redirect(url_for('index'))


@app.route("/successful")
def successful():
    return render_template("successful.html")

@app.route("/delete/<id>")
def delete(id):
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('DELETE FROM Productos WHERE ID = ?', (id,))
    con.commit()
    target.os.remove()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True)