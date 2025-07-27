export function validacion(form) {
    let nombres = form['nombres'];
    let apellidos = form['apellidos'];
    let telefono = form['telefono'];
    let valido = [true];

    nombres.classList.remove('is-invalid');
    apellidos.classList.remove('is-invalid');
    telefono.classList.remove('is-invalid');

    if (nombres.value.trim().length === 0) {
        nombres.classList.add('is-invalid');
        nombres.focus();
        valido.push(false);
    } else if (apellidos.value.trim().length === 0) {
        apellidos.classList.add('is-invalid');
        apellidos.focus();
        valido.push(false);
    } else if (telefono.value.trim().length === 0) {
        telefono.classList.add('is-invalid');
        telefono.focus();
        valido.push(false);
    }

    return valido.every(item => item === true);
}