export function cambiar() {
    let form = document.getElementById('form_agregar');
    let listar = document.getElementById('tbl_listar').parentElement;
    
    if (form.hidden) {
        form.hidden = false;
        listar.hidden = true;
    } else {
        form.hidden = true;
        listar.hidden = false;
    }
}
