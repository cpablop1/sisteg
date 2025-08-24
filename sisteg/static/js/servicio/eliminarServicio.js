import * as alerta from '../alertas/alertas.js';
import { editarServicio } from './EditarServicio.js';

export function eliminarServicio(datos) {
    let formData = new FormData()
    let servicio_id = document.getElementById('actualizar_servicio').getAttribute('servicio_id');
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
                editarServicio(servicio_id);
            }, 500);
        } else {
            alerta.danger(data.msg);
        }
    });
}