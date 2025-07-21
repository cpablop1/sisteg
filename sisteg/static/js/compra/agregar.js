import * as alerta from '../alertas/alertas.js';
import { listarCarrito } from './listarCarrito.js';

export function agregar(form, producto_id, cantidad) {
    let formData = new FormData(form)
    formData.append('producto_id', producto_id);
    formData.append('cantidad', cantidad);
    fetch('/compra/agregar-compra/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    }).then(res => {
        return res.json();
    }).then(data => {
        if (data.res) {
            alerta.success(data.msg);
            setTimeout(() => {
                listarCarrito();
            }, 500);
        } else {
            alerta.danger(data.msg);
        }
    });
}