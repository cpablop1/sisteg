import * as alerta from '../alertas/alertas.js';
import { cambiar } from "./cambiar.js";

export function confirmarServicio(data) {
    fetch(`/servicio/confirmar-servicio/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    }).then(res => res.json()).then(data => {
        if (data.res) {
            alerta.success(data.msg);
            //cambiar();
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
        alerta.danger('Hubo un error en el servidor.');
    });
}