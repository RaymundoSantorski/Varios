from flask import Flask, render_template, request, redirect, url_for, flash, session, escape, jsonify
import os, smtplib, sqlite3
from google.cloud import storage
from firebase import firebase 

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'static/')
total = 0

# firebase
db = firebase.FirebaseApplication('https://apapachatestore.firebaseio.com/')

#email smtp
emaillist = ['rayma9829@gmail.com',]
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

#storeManager
@app.route("/storeManager", methods =['POST','GET']) 
def storeManager():
    if "username" in session:
        data = db.get("Productos", "")
        name = escape(session["username"])
        return render_template("storeManager.html", it = data, opc = True, name = name )
    else:
        if request.method == 'POST':
            user = request.form['usuario']
            password = request.form['contrasena']
            usuarios = db.get("Usuarios", "")
            auten = False
            for key in usuarios:
                if usuarios[key]["Usuario"]==user and usuarios[key]["Contraseña"]==password:
                    session["username"] = user
                    auten = True
                    break
        
            if auten == True:   
                data = db.get("Productos", "")
                flash('Bienvenido')
                name = escape(session["username"])
                return render_template("storeManager.html", it = data, opc = True, name = name)
            else:
                flash('El usuario o la contraseña son incorrectos')
                return render_template("autenticar.html")
        else:
            return render_template("autenticar.html")

@app.route('/storeManager/logout')
def storeLogout():
    session.pop("username")
    flash('Has cerrado tu sesión')
    return redirect(url_for('storeManager'))

@app.route("/add", methods = ['POST'])
def add():
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        producto = request.form['producto']
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        inventario = request.form['inventario']
        etiquetas = request.form['etiquetas']
        filename = imagen.filename
        destination = "/".join([target, filename])
        if producto == "" or precio == "" or descripcion=="" or (imagen==None) or inventario == None or etiquetas == "":
            flash('Llena todos los campos correctamente')
            return redirect(url_for('storeManager'))
        else:
            filename = imagen.filename
            destination = "/".join([target, filename])
            precioFormat = int(precio)
            imagen.save(destination)
            data =  {
                    "Producto": producto,
                    "Imagen": filename,
                    "Descripcion": descripcion,
                    "Precio": precio,
                    "Inventario": inventario,
                    "Etiquetas": etiquetas
                    }
            db.post("Productos", data)
            server.login('apapachatestore@gmail.com','apapachatecontrasena')
            message = 'Se ha agregado un producto satisfactoriamente\nCorreo enviado desde apapachatestore.herokuapp.com'
            subject = 'Producto agregado'
            message = 'Subject: {}\n\n{}'.format(subject, message)
            for email in emaillist:
                server.sendmail('apapachatestore@gmail.com', email, message)
            flash('Producto agregado satisfactoriamente')
            return redirect(url_for('storeManager'))

@app.route("/delete/<id>")
def delete(id):
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('SELECT Imagen FROM Productos WHERE ID = ?', (id,))
    img = cur.fetchone()
    data = db.get("Productos", id)
    imagen = data[4]
    print(imagen)
    cur.execute('DELETE FROM Productos WHERE ID = ?', (id,))
    con.commit()
    os.remove('static/'+img[0])
    server.login('apapachatestore@gmail.com','apapachatecontrasena')
    message = 'El producto ha sido eliminado satisfactoriamente\nCorreo enviado desde apapachatestore.herokuapp.com'
    subject = 'Producto eliminado'
    message = 'Subject: {}\n\n{}'.format(subject, message)
    for email in emaillist:
        server.sendmail('apapachatestore@gmail.com', email, message)
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
        inventario = request.form['inventario']
        etiquetas = request.form['etiquetas']
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
        if inventario:
            cur.execute("UPDATE Productos SET Inventario = ? WHERE ID = ?", (inventario, id))
            con.commit()
        if etiquetas:
            cur.execute("UPDATE Productos SET Etiquetas = ? WHERE ID = ?", (etiquetas, id))
            con.commit()
        server.login('apapachatestore@gmail.com','apapachatecontrasena')
        message = 'El producto ha sido actualizado satisfactoriamente\nCorreo enviado desde apapachatestore.herokuapp.com'
        subject = 'Producto actualizado'
        message = 'Subject: {}\n\n{}'.format(subject, message)
        for email in emaillist:
            server.sendmail('apapachatestore@gmail.com', email, message)
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('storeManager'))

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':    
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        confirmcontrasena = request.form['confirmcontrasena']
        correo = request.form['email']
        users = db.get("Usuarios", "")
        registrar = False
        if contrasena == confirmcontrasena:
            for user in users:
                if users[user]["Usuario"] == usuario:
                    flash('El usuario ya existe, intente con otro')
                    return render_template('signup.html')
                else:
                    data =  {
                        "Usuario": usuario,
                        "Contraseña": contrasena,
                        "email": correo
                    }
                    db.post("Usuarios", data)
                    server.login('apapachatestore@gmail.com','apapachatecontrasena')
                    message = 'Se ha registrado un nuevo usuario\nCorreo enviado desde apapachatestore.herokuapp.com'
                    subject = 'Alta de usuario'
                    message = 'Subject: {}\n\n{}'.format(subject, message)
                    for email in emaillist:
                        server.sendmail('apapachatestore@gmail.com', email, message)
                    flash('Usuario registrado exitosamente')
                    return redirect(url_for('storeManager'))
        else:
            flash('Las contraseñas deben coincidir')
            return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route("/adduser", methods=['POST'])
def adduser():
    flash('Usuario registrado satisfactoriamente')
    return redirect(url_for('storeManager'))


#apapachateStore
@app.route("/")
def index():
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Productos")
    productos = cur.fetchall()
    return render_template('index.html', productos = productos)

@app.route("/productos")
def product():
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM Productos')
    data = cur.fetchall()
    return render_template("productos.html", productos = data)

@app.route("/vaciarCarrito")
def vaciarCarrito():
    session.pop("total")
    flash("Has vaciado el carrito")
    return render_template('carrito.html')

@app.route("/addproduct/<int:precio>")
def agregar(precio):
    if 'total' in session:
        session['total'] = int(escape(session['total']))+precio
    else:
        session['total'] = precio
    flash('El total es {}'.format(escape(session['total'])))
    return redirect(url_for('index'))


@app.route("/successful")
def successful():
    return render_template("successful.html")

@app.route("/carrito")
def carrito():
    if 'total' in session:
        return render_template('carrito.html', total = escape(session['total']))
    else:
        return render_template('carrito.html')

@app.route("/producto/<id>")
def producto(id):
    con = sqlite3.connect('mydb.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Productos WHERE ID = ?", (id,))
    producto = cur.fetchall()
    return render_template("producto.html", productos = producto)


if __name__ == '__main__': 
    app.run(debug=True, port=5500)