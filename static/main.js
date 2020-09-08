var total = 0;
var btnActivar = document.getElementById("activar");

function agregar(){
    var elemento = document.getElementById("overlay");
    elemento.classList.add('active');
}

function remover(){
    var elemento = document.getElementById("overlay");
    elemento.classList.remove('active');
}

function add(Producto, precio){
    var dv = document.createElement("div");
    dv.id = Producto;
    dv.name = Producto;
    var element = document.createElement("label");
    var btn = document.createElement("button");
    btn.textContent = "X"
    btn.classList.add("boton"); 
    btn.addEventListener('click',function(){
        var eli = document.getElementsByName(Producto);
        var pa = document.getElementById(Producto);
        pa.remove(eli);
        total=total-precio;
        document.getElementById("total").innerHTML = "El total es: $"+total;
    });
    document.querySelector(".items").appendChild(dv);
    element.innerHTML = Producto + " $" + precio
    dv.appendChild(element);    
    dv.appendChild(btn);
    

    total = total + parseFloat(precio);
    document.getElementById("total").innerHTML = "El total es: $"+total;
    
}
