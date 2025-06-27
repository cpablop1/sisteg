import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { listar } from './listar.js';
import { listarCarrito } from './listarCarrito.js';

export function agregar(form, producto_id) {
    let formData = new FormData(form)
    formData.append('producto_id', producto_id);
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