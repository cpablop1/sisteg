export function validacion(form) {
    let cliente_id = form['cliente_id'];
    let tipo_pago_id = form['tipo_pago_id'];
    let tipo_servicio_id = form['tipo_servicio_id'];
    let valido = [];

    // Limpiar clases de validación
    [cliente_id, tipo_pago_id, tipo_servicio_id].forEach(field => {
        if (field) {
            field.classList.remove('is-invalid');
        }
    });

    // Validar cliente
    if (cliente_id.value.trim().length === 0) {
        cliente_id.classList.add('is-invalid');
        cliente_id.focus();
        valido.push(false);
    }

    // Validar tipo de pago
    if (tipo_pago_id.value.trim().length === 0) {
        tipo_pago_id.classList.add('is-invalid');
        tipo_pago_id.focus();
        valido.push(false);
    }

    // Validar tipo de servicio
    if (tipo_servicio_id.value.trim().length === 0) {
        tipo_servicio_id.classList.add('is-invalid');
        tipo_servicio_id.focus();
        valido.push(false);
    }

    // Validar que sea venta (id = 1)
    if (tipo_servicio_id.value !== '1') {
        tipo_servicio_id.classList.add('is-invalid');
        tipo_servicio_id.focus();
        valido.push(false);
    }

    return valido.length === 0;
}