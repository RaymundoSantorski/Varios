var btnActivar = document.getElementById("activar");

function agregar(){
    var elemento = document.getElementById("overlay");
    elemento.classList.add('active');
}

function remover(){
    var elemento = document.getElementById("overlay");
    elemento.classList.remove('active');
}

function add(){
    var element = document.createElement("label");
    element.innerHTML = "Producto"
    /*document.getElementById("items").innerHTML = document.getElementById("items").innerHTML + "\n"+"Producto";*/
    document.querySelector(".items").appendChild(element);
    
}