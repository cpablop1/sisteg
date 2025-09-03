import * as alerta from '../alertas/alertas.js';

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
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
    })
}