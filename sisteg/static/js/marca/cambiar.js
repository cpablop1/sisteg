// Evento para cambiar de vista entre el formulario y el listado de categoría
export function cambiar() {
    let btn_agregar = document.getElementById('agregar');
    let form_agregar = document.getElementById('form_agregar');
    let listar = document.getElementById('listar');

    if (listar.hidden) {
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        form_agregar.reset();
        listar.hidden = false;
        form_agregar.hidden = true;
    } else {
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        form_agregar.reset();
        listar.hidden = true;
        form_agregar.hidden = false;
        document.getElementById('descripcion').focus();
    }
}