import * as alerta from '../alertas/alertas.js';
import { editarServicio } from './EditarServicio.js';

export function agregar(form, producto_id, cantidad, costo, precio) {
    let formData = new FormData(form)
    formData.append('producto_id', producto_id);
    formData.append('cantidad', cantidad);
    formData.append('costo', costo);
    formData.append('precio', precio);
    formData.append('servicio_id', document.getElementById('actualizar_servicio').getAttribute('servicio_id'));
    fetch('/servicio/agregar-servicio/', {
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
            editarServicio(formData.get('servicio_id'));
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
    })
}