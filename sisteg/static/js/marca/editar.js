import { cambiar } from "./cambiar.js";

export function editar(id) {
    cambiar();
    fetch(`/producto/listar-marca/?id=${id}`).then(res => res.json()).then(data => {
        let id = document.querySelector('#form_agregar input[name=id]');
        let descripcion = document.querySelector('#form_agregar input[name=descripcion]');

        id.value = data.data[0].id;
        descripcion.value = data.data[0].descripcion;
    });
}