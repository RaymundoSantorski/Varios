from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)

#conección a sqlite3

# settings
app.secret_key = 'mysecretkey'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'static/')
total = 0
loggeado = False

@app.route("/")
def index():
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Productos")
    productos = cur.fetchall()
    return render_template('index.html', productos = productos)

@app.route("/storeManager", methods =['POST','GET']) 
def storeManager():
    global loggeado
    if loggeado == False:
        if request.method == 'POST':
            user = request.form['usuario']
            password = request.form['contrasena']
            con = sqlite3.connect('mydb.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM Usuarios')
            usuarios = cur.fetchall()
            auten = False
            for usuario in usuarios:
                if usuario[1]==user and usuario[0]==password:
                    auten = True
                    break
        
            if auten == True:   
                cur.execute('SELECT * FROM Productos')
                data = cur.fetchall()
                loggeado = True
                flash('Bienvenido')
                return render_template("storeManager.html", productos = data)
            else:
                flash('El usuario o la contraseña son incorrectos')
                return render_template("autenticar.html")
        else:
            return render_template("autenticar.html")
    else:
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM Productos')
        data = cur.fetchall()
        return render_template("storeManager.html", productos = data )

@app.route("/productos")
def product():
    return render_template("producto.html")

@app.route("/add", methods = ['POST'])
def add():
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        producto = request.form['producto']
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        filename = imagen.filename
        destination = "/".join([target, filename])
        if producto == "" or precio == "" or descripcion=="" or (imagen==None):
            return "Formato no valido"
        else:
            filename = imagen.filename
            destination = "/".join([target, filename])
            precioFormat = int(precio)
            imagen.save(destination)
            con = sqlite3.connect('mydb.db')
            cur = con.cursor()
            cur.execute('INSERT INTO Productos (Producto, Imagen, Descripcion, Precio) VALUES (?,?,?,?)',(producto, filename, descripcion, precio))
            con.commit()
            flash('Producto agregado satisfactoriamente')
            return redirect(url_for('storeManager'))


@app.route("/addproduct/<int:precio>")
def agregar(precio):
    global total 
    total += precio
    flash('El total es {}'.format(total))
    return redirect(url_for('index'))

@app.route("/successful")
def successful():
    return render_template("successful.html")

@app.route("/delete/<id>")
def delete(id):
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('SELECT Imagen FROM Productos WHERE ID = ?', (id,))
    img = cur.fetchone()
    cur.execute('DELETE FROM Productos WHERE ID = ?', (id,))
    con.commit()
    os.remove('static/'+img[0])
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('storeManager'))

@app.route("/edit/<id>")
def edit(id):
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM Productos WHERE ID = ?', (id,))
    data = cur.fetchone()
    return render_template("edit.html", producto = data)

@app.route("/update/<id>", methods = ['POST'])
def update(id):
    if request.method == 'POST':
        producto = request.form['producto']
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        filename = imagen.filename
        destination = "/".join([target, filename])
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        if imagen:
            cur.execute('SELECT Imagen FROM Productos WHERE ID = ?', (id,)) 
            ind = cur.fetchone()
            img = ind[0]
            os.remove('static/'+img)
            cur.execute("""
                UPDATE Productos
                SET Imagen = ?
                WHERE ID = ?
            """, (filename, id))
            con.commit()
            imagen.save(destination)
        if producto:
            cur.execute("UPDATE Productos SET Producto = ? WHERE ID = ?", (producto, id))
            con.commit()
        if descripcion:
            cur.execute("UPDATE Productos SET descripcion = ? WHERE ID = ?", (descripcion, id))
            con.commit()
        if precio:
            precioFormat = int(precio)
            cur.execute("UPDATE Productos SET Precio = ? WHERE ID = ?", (precioFormat   , id))
            con.commit()
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('storeManager'))

if __name__ == '__main__': 
    app.run(debug=True)