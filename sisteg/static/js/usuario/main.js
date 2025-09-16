import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { editar } from './editar.js';
import { validacion } from './validacion.js';
import { llenarSelectRoles } from './listarRolUsuario.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-user"></i> Usuario`;
    listar();
}

window.listar = (data) => {
    listar(data);
}

// Evento para cambiar de vista entre el formulario y el listado de usuarios
document.getElementById('agregar').addEventListener('click', e => {
    cambiar();
    // Cargar roles cuando se muestre el formulario
    const rolSelect = document.getElementById('rol');
    if (rolSelect) {
        llenarSelectRoles(rolSelect, 'Seleccione un rol');
    }
});

// Evento para agregar usuario
document.getElementById('form_agregar').addEventListener('submit', e => {
    e.preventDefault();
    let form = e.target;
    if (validacion(form)) {
        agregar(form)
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para editar marca
document.getElementById('tbl_listar').addEventListener('click', e => {
    let id = parseInt(e.target.getAttribute('editar'))
    if (id) {
        editar(id);
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