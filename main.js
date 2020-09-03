var btnActivar = document.getElementById("activar");

function agregar(){
    var elemento = document.getElementById("overlay");
    elemento.classList.add('active');
}

function remover(){
    var elemento = document.getElementById("overlay");
    elemento.classList.remove('active');
}