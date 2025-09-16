import * as alerta from '../alertas/alertas.js';

export function garantiaServicio() {
    const form = document.getElementById('form_garantia');
    const formData = new FormData(form);
    
    fetch('/servicio/garantia-servicio/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.res) {
            alerta.success(data.msg);
            form.reset();
        } else {
            alerta.danger(data.msg);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alerta.danger('Error al procesar la garantía');
    });
}
