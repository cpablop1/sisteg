import * as alerta from '../alertas/alertas.js';
import { selectCliente } from './selectCliente.js';

export function agregarCliente(form) {
    let formData = new FormData(form)
    fetch('/servicio/agregar-cliente/', {
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
            bootstrap.Modal.getInstance(document.getElementById('mdl_agregar_cliente')).hide();
            setTimeout(() => {
                selectCliente();
            }, 500);
        } else {
            alerta.danger(data.msg);
        }
    });
}