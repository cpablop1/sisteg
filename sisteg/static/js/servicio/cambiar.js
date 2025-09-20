import { selectCliente } from "./selectCliente.js";
import { selectTipoPago } from "./selectTipoPago.js";
import { selectTipoServicio } from "./selectTipoServicio.js";
import { selectRolUsuario } from "./selectRolUsuario.js";

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
    } else {
        btn_agregar.innerHTML = '<a href="/servicio" class="decoration-none text-dark"><i class="fa-solid fa-circle-left"></i></a>';
        listar.hidden = true;
        form_agregar.hidden = false;
    }

    selectCliente();
    selectTipoPago();
    selectTipoServicio();
    selectRolUsuario();
}