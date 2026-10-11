import * as alerta from '../../alertas/alertas.js';

export function agregar(form) {
    let formData = new FormData(form);
    let data = {};

    // Recopilar datos del formulario
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    // Agregar tipo de servicio fijo para mantenimiento (excluyendo venta)
    data.tipo_servicio_id = form.querySelector('#tipo_servicio_id').value;

    // Establecer costo del servicio en 0 (se maneja en la vista del técnico)
    formData.set('costo_servicio', '0');

    // Obtener análisis generado por IA
    const analisisIa = window.obtenerAnalisisIaMantenimiento
        ? window.obtenerAnalisisIaMantenimiento()
        : null;

    // Solamente se envía si el usuario generó y conservó un análisis
    if (analisisIa) {
        formData.set(
            'analisis_ia',
            JSON.stringify(analisisIa)
        );
    }

    // Validar que se haya seleccionado un tipo de servicio de mantenimiento
    if (data.tipo_servicio_id == '1') {
        alerta.warning('Esta vista es solo para servicios de mantenimiento. Use la vista de Venta para ventas.');
        return;
    }

    fetch('/servicio/agregar-servicio/', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.res) {
                alerta.success(data.msg);
                form.reset();
                // Actualizar subtotal
                document.getElementById('subtotal').textContent = 'Q. 00';
                document.getElementById('ganancia').textContent = 'Q. 00';
            } else {
                alerta.danger(data.msg);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alerta.danger('Error al procesar la solicitud');
        });
}

export function actualizar(form, servicio_id) {
    let formData = new FormData(form);
    let data = {};

    // Recopilar datos del formulario
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    // Agregar tipo de servicio fijo para mantenimiento (excluyendo venta)
    data.tipo_servicio_id = form.querySelector('#tipo_servicio_id').value;

    // Establecer costo del servicio en 0 (se maneja en la vista del técnico)
    formData.set('costo_servicio', '0');

    // Obtener análisis generado por IA
    const analisisIa = window.obtenerAnalisisIaMantenimiento
        ? window.obtenerAnalisisIaMantenimiento()
        : null;

    /*
    * Si hay un análisis nuevo, se envía.
    * Si no existe, no se envía el campo para evitar borrar
    * accidentalmente un análisis guardado anteriormente. 
    */
    if (analisisIa) {
        formData.set(
            'analisis_ia',
            JSON.stringify(analisisIa)
        );
    }

    // Agregar servicio_id para actualización
    formData.set('servicio_id', servicio_id);

    // Validar que se haya seleccionado un tipo de servicio de mantenimiento
    if (data.tipo_servicio_id == '1') {
        alerta.warning('Esta vista es solo para servicios de mantenimiento. Use la vista de Venta para ventas.');
        return;
    }

    fetch('/servicio/agregar-servicio/', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.res) {
                alerta.success(data.msg);
                form.reset();
                // Actualizar subtotal
                document.getElementById('subtotal').textContent = 'Q. 00';
                document.getElementById('ganancia').textContent = 'Q. 00';
            } else {
                alerta.danger(data.msg);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alerta.danger('Error al procesar la solicitud');
        });
}
