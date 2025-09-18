import * as alerta from '../alertas/alertas.js';
import { listarDetalleServicio } from './listarDetalleServicio.js';
import { verGarantia } from './verGarantia.js';

export function garantiaServicio() {
    let form = document.getElementById('form_garantia');
    let formData = new FormData(form)
    fetch('/servicio/garantia-servicio/', {
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
            console.log(data);
            setTimeout(() => {
                verGarantia(data.garantia_id);
                listarDetalleServicio(data.servicio_id);
            }, 500);
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
    })
}