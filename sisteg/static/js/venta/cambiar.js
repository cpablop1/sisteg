import { listarCarrito } from "./listarCarrito.js";
import { selectCliente } from "./selectCliente.js";
import { selectTipoPago } from "./selectTipoPago.js";
import { listar as listado} from './listar.js';

// Evento para cambiar de vista entre el formulario y el listado de categoría
export function cambiar() {
    let btn_agregar = document.getElementById('agregar');
    let form_agregar = document.getElementById('form_agregar');
    let listar = document.getElementById('listar');

    form_agregar.reset();

    if (listar.hidden) {
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        listar.hidden = false;
        form_agregar.hidden = true;
        listado();
    } else {
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        listar.hidden = true;
        form_agregar.hidden = false;
        listarCarrito();
    }

    selectCliente();
    selectTipoPago();
}