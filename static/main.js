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
    dv.classList.add('item');
    var element = document.createElement("label");
    var btn = document.createElement("input");
    btn.type = "button";
    btn.addEventListener('click',function(){
        var padre = this.parentNode().id
        alert("funciona");
    });
    document.querySelector(".items").appendChild(dv);
    element.innerHTML = Producto + " $" + precio
    document.querySelector(".item").appendChild(element);    
    document.querySelector(".item").appendChild(btn);
    

    total = total + parseFloat(precio);
    document.getElementById("total").innerHTML = "El total es: $"+total;
    
}
