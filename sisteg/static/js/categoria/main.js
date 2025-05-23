import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { editar } from './editar.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-tags"></i> Categoría`;
    listar();
}

window.listar = (data) => {
    listar(data);
}

// Evento para cambiar de vista entre el formulario y el listado de categoría
document.getElementById('agregar').addEventListener('click', e => {
    cambiar();
});

// Evento para agregar categoría
document.getElementById('form_agregar').addEventListener('submit', e => {
    e.preventDefault();
    let descripcion = e.target.querySelector('#descripcion');
    if (descripcion.value.trim().length === 0) { // Evaluamos si no está vacío el campo
        alerta.danger('Complete el formulario para continuar.');
        descripcion.classList.add('is-invalid');
    } else {
        descripcion.classList.remove('is-invalid');
        agregar(e.target);
    }
});

// Evento para editar categoría
document.getElementById('tbl_listar').addEventListener('click', e => {
    let id = parseInt(e.target.getAttribute('editar'))
    if (id) {
        editar(id);
    }
});

// Evento para buscar categorías
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({'pagina': 1, 'buscar': buscar });
    } else {
        listar();
    }
});