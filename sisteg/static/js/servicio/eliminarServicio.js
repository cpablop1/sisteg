import * as alerta from '../alertas/alertas.js';
import { listarCarrito } from './listarCarrito.js';

export function eliminarServicio(datos) {
    let formData = new FormData()
    Object.entries(datos).forEach(([clave, valor]) => {
        formData.append(clave, valor);
    });
    fetch('/servicio/eliminar-servicio/', {
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