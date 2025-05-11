window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-brands fa-product-hunt"></i> Producto`;

}

document.getElementById('agregar').addEventListener('click', e => {
    let btn_agregar = document.getElementById('agregar');
    let form_agregar = document.getElementById('form_agregar');
    let listar = document.getElementById('listar');

    if (listar.hidden) {
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        listar.hidden = false;
        form_agregar.hidden = true;
    } else {
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        listar.hidden = true;
        form_agregar.hidden = false;
    }
});