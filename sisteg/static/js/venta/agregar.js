import * as alerta from '../alertas/alertas.js';
import { listarCarrito } from './listarCarrito.js';

export function agregar(form, producto_id, cantidad) {
    let formData = new FormData(form)
    formData.append('producto_id', producto_id);
    formData.append('cantidad', cantidad);
    fetch('/servicio/agregar-servicio/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    }).then(res => {
        return res.json();
    }).then(data => {
        console.log(data);
        if (data.res) {
            alerta.success(data.msg);
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
    }).finally(e => {
        setTimeout(() => {
            listarCarrito();
        }, 500);
    });
}