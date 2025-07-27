import { cambiar } from "./cambiar.js";

export function editar(id) {
    cambiar();
    fetch(`/compra/listar-proveedor/?id=${id}`).then(res => res.json()).then(data => {
        let inputs = ['id', 'nombres', 'apellidos', 'nit', 'cui', 'telefono', 'direccion', 'correo', 'empresa'];
        setTimeout(() => {
            Array.from(inputs, value => {
                document.getElementById(value).value = data.data[0][value];
            });
        }, 1000);
    });
}