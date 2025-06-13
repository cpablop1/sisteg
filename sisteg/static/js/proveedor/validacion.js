export function validacion(form) {
    let descripcion = form['descripcion'];
    let marca = form['marca_id'];
    let categoria = form['categoria_id'];
    let valido = [true];

    descripcion.classList.remove('is-invalid');
    marca.classList.remove('is-invalid');
    categoria.classList.remove('is-invalid');

    if (descripcion.value.trim().length === 0) {
        descripcion.classList.add('is-invalid');
        descripcion.focus();
        valido.push(false);
    } else if (marca.value.trim().length === 0) {
        marca.classList.add('is-invalid');
        marca.focus();
        valido.push(false);
    } else if (categoria.value.trim().length === 0) {
        categoria.classList.add('is-invalid');
        categoria.focus();
        valido.push(false);
    }

    return valido.every(item => item === true);
}