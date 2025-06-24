import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { editar } from './editar.js';
import { validacion } from './validacion.js';
import { listarProductos } from './listarProductos.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-basket-shopping"></i> Compra`;
    listar();
}

window.listar = (data) => {
    listar(data);
}

window.listarProductos = (data) => {
    listarProductos(data);
}

// Evento para buscar productos
document.getElementById('buscar_productos').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listarProductos({ 'pagina': 1, 'buscar': buscar });
    } else {
        listarProductos();
    }
});

// Evento para cambiar de vista entre el carrito y el listado de compras
document.getElementById('agregar').addEventListener('click', e => {
    cambiar();
});

// Evento para confirmar compra
document.getElementById('form_agregar').addEventListener('submit', e => {
    e.preventDefault();
    let form = e.target;
    if (validacion(form)) {
        agregar(form)
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para mostrar modal de buscar productos
document.getElementById('btn-buscar-productos').addEventListener('click', e => {
    new bootstrap.Modal(document.getElementById('mdl_buscar_productos')).show();
    setTimeout(() => listarProductos(), 500);
});

// Evento para agregar productos al carrito
document.getElementById('tbl_listar_productos').addEventListener('click', e => {
    let id = parseInt(e.target.getAttribute('agregar'))
    let form = document.getElementById('form_agregar');
    console.log(id);
    console.log(validacion(form));
    if (id && validacion(form)) {
        console.log(id);
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para buscar marcas
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({ 'pagina': 1, 'buscar': buscar });
    } else {
        listar();
    }
});