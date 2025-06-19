export function validacion(form) {
    let proveedor_id = form['proveedor_id'];
    let tipo_pago_id = form['tipo_pago_id'];
    let valido = [true];

    proveedor_id.classList.remove('is-invalid');
    tipo_pago_id.classList.remove('is-invalid');

    if (proveedor_id.value.trim().length === 0) {
        proveedor_id.classList.add('is-invalid');
        proveedor_id.focus();
        valido.push(false);
    } else if (tipo_pago_id.value.trim().length === 0) {
        tipo_pago_id.classList.add('is-invalid');
        tipo_pago_id.focus();
        valido.push(false);
    }

    return valido.every(item => item === true);
}