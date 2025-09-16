import * as alerta from '../alertas/alertas.js';

export function eliminarGarantia(data) {
    const formData = new FormData();
    
    if (data.detalle_garantia_id) {
        formData.append('detalle_garantia_id', data.detalle_garantia_id);
    }
    if (data.garantia_id) {
        formData.append('garantia_id', data.garantia_id);
    }
    
    fetch('/servicio/eliminar-garantia/', {
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
        alerta.danger('Error al eliminar la garantía');
    });
}
