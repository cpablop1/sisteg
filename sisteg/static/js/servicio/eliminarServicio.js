import * as alerta from '../alertas/alertas.js';

export function eliminarServicio(data) {
    const formData = new FormData();
    
    if (data.detalle_servicio_id) {
        formData.append('detalle_servicio_id', data.detalle_servicio_id);
    }
    if (data.servicio_id) {
        formData.append('servicio_id', data.servicio_id);
    }
    
    // Agregar token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    fetch('/servicio/eliminar-servicio/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.res) {
            alerta.success(data.msg);
        } else {
            alerta.danger(data.msg);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alerta.danger('Error al eliminar el servicio');
    });
}