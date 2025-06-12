import { cambiar } from "./cambiar.js";

export function editar(id) {
    cambiar();
    fetch(`/producto/listar-producto/?id=${id}`).then(res => res.json()).then(data => {
        let inputs = ['id', 'descripcion', 'detalle', 'costo', 'precio', 'stock', 'marca_id', 'categoria_id'];
        setTimeout(() => {
            Array.from(inputs, value => {
                console.log(data.data[0][value]);
                console.log(document.getElementById(value));
                document.getElementById(value).value = data.data[0][value];
            });
        }, 1000);
    });
}