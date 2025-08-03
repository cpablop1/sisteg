export function validacion(form) {
    let cliente_id = form['cliente_id'];
    let tipo_pago_id = form['tipo_pago_id'];
    let valido = [true];

    cliente_id.classList.remove('is-invalid');
    tipo_pago_id.classList.remove('is-invalid');

    if (cliente_id.value.trim().length === 0) {
        cliente_id.classList.add('is-invalid');
        cliente_id.focus();
        valido.push(false);
    } else if (tipo_pago_id.value.trim().length === 0) {
        tipo_pago_id.classList.add('is-invalid');
        tipo_pago_id.focus();
        valido.push(false);
    }

    return valido.every(item => item === true);
}