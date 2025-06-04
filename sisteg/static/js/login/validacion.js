export function validacion(usuario_input, clave_input) {
    let usuario = usuario_input.value.trim();
    let clave = clave_input.value.trim();

    usuario_input.classList.remove('is-invalid');
    clave_input.classList.remove('is-invalid');

    if (usuario.length === 0) {
        usuario_input.classList.add('is-invalid');
        usuario_input.focus();
        return false;
    } else if (clave.length === 0) {
        clave_input.classList.add('is-invalid');
        clave_input.focus();
        return false;
    } else {
        return true;
    }
}