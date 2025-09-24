import * as alerta from '../alertas/alertas.js';

export function eliminarGarantia(data) {
    let formData = new FormData()
    formData.append('detalle_garantia_id', data.detalle_garantia_id);
    formData.append('garantia_id', data.garantia_id);
    fetch('/servicio/eliminar-garantia/', {
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
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        alerta.danger('Error en el servidor.');
    })
}