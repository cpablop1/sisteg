import { selectMarca } from './selectMarca.js';
import { selectCategoria } from './selectCategoria.js';

// Evento para cambiar de vista entre el formulario y el listado de categoría
export function cambiar() {
    let btn_agregar = document.getElementById('agregar');
    let form_agregar = document.getElementById('form_agregar');
    let listar = document.getElementById('listar');

    document.getElementById('ver_img1').innerHTML = '';
    document.getElementById('ver_img2').innerHTML = '';
    form_agregar.reset();

    if (listar.hidden) {
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        listar.hidden = false;
        form_agregar.hidden = true;
    } else {
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        listar.hidden = true;
        form_agregar.hidden = false;
        document.getElementById('descripcion').focus();
    }
    selectMarca();
    selectCategoria();
}