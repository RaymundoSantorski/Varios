var total=0

function active(elem){
	var nab = document.getElementById(elem);
	var nabs = documents.getElementsByClassName('nav-link active');
	nabs.array.forEach(element => {
		element.classList.remove('nav-link active');
		element.classList.add('nav-link');
	});
	nab.classList.remove('nav-link');
	nab.classList.add('nav-link active');
}

function info(precio)
{
	alert("El precio es $"+precio)
}

function add(precio)
{
	total = total+precio;
	console.log(total)
	
}

function cerrar(){
	var pop = document.getElementById("sucess");
	pop.classList.remove('active');
}

function carrito()
{
	document.getElementById("total").innerHTML = "Total: $"+total;
	var elemento = document.getElementById("overlay");
	elemento.classList.add('active');
}

function cerrarCarrito()
{
	var elemento = document.getElementById("overlay");
	elemento.classList.remove('active');
}

function sucess(name){
	document.getElementById("mensaje").innerHTML = "Gracias por tu compra "+name+"!";
	var men = document.getElementById("sucess");
	var over = document.getElementById("overlay");
	men.classList.add("active");
	over.classList.remove("active");
	total = 0;
	document.getElementById("total").innerHTML = null;
	var elim = document.getElementsByClassName("it");
	elim.remove();

}
