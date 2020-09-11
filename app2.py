from flask import Flask, render_template, request

app = Flask(__name__) 

@app.route("/") 
def index(): 
    return render_template("index.html")

@app.route("/productos")
def product():
    return render_template("producto.html")

@app.route("/carrito", methods = ['GET','POST'])
def carrito():
    return render_template("carrito.html")
    if request.method == 'POST':
        return "Eres grandioso"


@app.route("/successful")
def successful():
    return render_template("successful.html")


if __name__ == '__main__': 
    app.run(debug=True)