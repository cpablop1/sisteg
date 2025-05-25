import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { listar } from './listar.js';

export function agregar(form) {
    let formData = new FormData(form)
    fetch('/producto/agregar-marca/', {
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
            cambiar();
            setTimeout(() => {
                listar();
            }, 500);
        } else {
            alerta.danger(data.msg);
        }
    });
}