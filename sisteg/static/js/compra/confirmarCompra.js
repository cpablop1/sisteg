import { cambiar } from "./cambiar.js";

export function confirmarCompra(data) {
    fetch(`/compra/confirmar-compra/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    }).then(res => res.json()).then(data => {
        console.log(data);
    });
}