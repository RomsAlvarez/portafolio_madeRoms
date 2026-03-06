let carrito = JSON.parse(localStorage.getItem("carrito")) || []

const botones = document.querySelectorAll(".agregar")

botones.forEach(boton => {

boton.addEventListener("click", () => {

const producto = {
nombre: boton.dataset.nombre,
precio: boton.dataset.precio
}

carrito.push(producto)

localStorage.setItem("carrito", JSON.stringify(carrito))

actualizarContador()

})

})

function actualizarContador(){

const contador = document.querySelector("#contador")

if(contador){
contador.textContent = carrito.length
}

}

actualizarContador()

const lista = document.querySelector("#lista-carrito")

if(lista){

carrito.forEach(producto => {

const li = document.createElement("li")

li.textContent = producto.nombre + " - $" + producto.precio

lista.appendChild(li)

})

}

const botonVaciar = document.querySelector("#vaciar-carrito");

if(botonVaciar){
  botonVaciar.addEventListener("click", function(){

    localStorage.removeItem("carrito");

    location.reload();

  });
}