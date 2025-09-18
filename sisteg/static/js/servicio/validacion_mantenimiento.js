export function validacion(form) {
    let cliente_id = form['cliente_id'];
    let tipo_pago_id = form['tipo_pago_id'];
    let tipo_servicio_id = form['tipo_servicio_id'];
    let rol_usuario_id = form['rol_usuario_id'];
    let observacion = form['observacion'];
    
    let valido = [];
    
    // Limpiar clases de validación
    [cliente_id, tipo_pago_id, tipo_servicio_id, rol_usuario_id, observacion].forEach(field => {
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
    
    // Validar que no sea venta
    if (tipo_servicio_id.value === '1') {
        tipo_servicio_id.classList.add('is-invalid');
        tipo_servicio_id.focus();
        valido.push(false);
    }
    
    // Validar técnico
    if (rol_usuario_id.value.trim().length === 0) {
        rol_usuario_id.classList.add('is-invalid');
        rol_usuario_id.focus();
        valido.push(false);
    }
    
    // Validar observación (obligatoria para mantenimiento)
    if (observacion.value.trim().length === 0) {
        observacion.classList.add('is-invalid');
        observacion.focus();
        valido.push(false);
    }
    
    // El costo del servicio se maneja en la vista del técnico, no aquí
    
    return valido.length === 0;
}
