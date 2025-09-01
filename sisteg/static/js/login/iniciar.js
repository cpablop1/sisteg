import * as alerta from '../alertas/alertas.js';
import { validacion } from "./validacion.js";

export function iniciar(form) {
    let usuario = document.getElementById('usuario');
    let clave = document.getElementById('clave');

    if (validacion(usuario, clave)) {
        let formData = new FormData(form)
        fetch('/autenticacion/iniciar/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData
        }).then(res => {
            return res.json();
        }).then(data => {
            if (data.res) {
                window.location.href = '/';
            } else {
                alerta.danger(data.msg);
            }
        });
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
}