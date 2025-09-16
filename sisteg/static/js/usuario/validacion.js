/**
 * Valida los campos del formulario de creación de usuario.
 * 
 * Esta función valida los campos requeridos y opcionales del formulario
 * de usuario, aplicando reglas de validación específicas para cada campo
 * y proporcionando retroalimentación visual al usuario mediante clases CSS.
 * 
 * @param {HTMLFormElement} form - El elemento formulario que contiene los campos a validar
 * @returns {boolean} true si todos los campos son válidos, false si hay errores
 * 
 * @example
 * // Ejemplo de uso con un formulario
 * const form = document.getElementById('form_agregar');
 * if (validacion(form)) {
 *     // Proceder con el envío del formulario
 *     enviarFormulario(form);
 * } else {
 *     // Mostrar mensaje de error
 *     alert('Por favor, corrija los errores en el formulario');
 * }
 * 
 * @since 1.0.0
 * @author Sistema de Gestión
 */
export function validacion(form) {
    // Obtener referencias a los elementos del formulario
    let username = form['username'];
    let password = form['password'];
    let first_name = form['first_name'];
    let last_name = form['last_name'];
    let email = form['email'];
    let rol = form['rol'];
    let valido = [true];

    // Limpiar clases de validación previas
    username.classList.remove('is-invalid');
    password.classList.remove('is-invalid');
    first_name.classList.remove('is-invalid');
    last_name.classList.remove('is-invalid');
    email.classList.remove('is-invalid');
    rol.classList.remove('is-invalid');

    /**
     * Valida el campo username.
     * Reglas: requerido, mínimo 3 caracteres
     */
    if (username.value.trim().length === 0) {
        username.classList.add('is-invalid');
        username.focus();
        valido.push(false);
    } else if (username.value.trim().length < 3) {
        username.classList.add('is-invalid');
        username.focus();
        valido.push(false);
    }

    /**
     * Valida el campo password.
     * Reglas: requerido solo si no hay ID (creación), mínimo 6 caracteres si se proporciona
     */
    const userIdField = form['id'];
    const userId = userIdField ? userIdField.value.trim() : '';
    
    if (!userId && password.value.trim().length === 0) {
        // Solo requerido para nuevos usuarios
        password.classList.add('is-invalid');
        password.focus();
        valido.push(false);
    } else if (password.value.trim().length > 0 && password.value.trim().length < 6) {
        // Si se proporciona password, debe tener al menos 6 caracteres
        password.classList.add('is-invalid');
        password.focus();
        valido.push(false);
    }

    /**
     * Valida el campo email.
     * Reglas: opcional, pero si se proporciona debe tener formato válido
     * Utiliza expresión regular para validar formato de email
     */
    if (email.value.trim().length > 0) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value.trim())) {
            email.classList.add('is-invalid');
            email.focus();
            valido.push(false);
        }
    }

    /**
     * Valida el campo rol.
     * Reglas: requerido, debe seleccionar una opción válida
     */
    if (rol.value.trim() === '') {
        rol.classList.add('is-invalid');
        rol.focus();
        valido.push(false);
    }

    // Los campos first_name y last_name son opcionales, no requieren validación

    return valido.every(item => item === true);
}