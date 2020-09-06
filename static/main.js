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
    
    document.getElementById("items").innerHTML = document.getElementById("items").innerHTML + "\n"+"Producto";
    
}