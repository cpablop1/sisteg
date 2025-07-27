import { cambiar } from "./cambiar.js";

export function editar(id) {
    cambiar();
    fetch(`/servicio/listar-cliente/?id=${id}`).then(res => res.json()).then(data => {
        let inputs = ['id', 'nombres', 'apellidos', 'nit', 'cui', 'telefono', 'direccion', 'correo'];
        setTimeout(() => {
            Array.from(inputs, value => {
                document.getElementById(value).value = data.data[0][value];
            });
        }, 1000);
    });
}