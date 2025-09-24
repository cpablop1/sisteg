/**
 * Obtiene la lista de roles de usuario disponibles desde el servidor.
 * 
 * Esta función hace una petición GET al endpoint de listar roles de usuario
 * y retorna los datos para ser utilizados en formularios o listados.
 * 
 * @returns {Promise<Object>} Promise que resuelve con los datos de roles
 * @example
 * // Ejemplo de uso
 * listarRolUsuario().then(data => {
 *     if (data.res) {
 *         console.log('Roles disponibles:', data.data);
 *     } else {
 *         console.error('Error:', data.msg);
 *     }
 * });
 * 
 * @since 1.0.0
 * @author Sistema de Gestión
 */
export function listarRolUsuario() {
    return fetch(`/autenticacion/listar-roles/`)
        .then(res => res.json())
        .then(data => {
            if (data.res) {
                return data;
            } else {
                return data;
            }
        })
        .catch(error => {
            console.error('Error de conexión:', error);
            return { res: false, msg: 'Error de conexión', data: [] };
        });
}

/**
 * Llena un elemento select con los roles de usuario disponibles.
 * 
 * @param {HTMLSelectElement} selectElement - Elemento select a llenar
 * @param {string} placeholder - Texto para la opción por defecto
 * @returns {Promise<void>}
 * 
 * @example
 * // Ejemplo de uso
 * const rolSelect = document.getElementById('rol');
 * llenarSelectRoles(rolSelect, 'Seleccione un rol');
 */
export function llenarSelectRoles(selectElement, placeholder = 'Seleccione un rol') {
    // Limpiar opciones existentes
    selectElement.innerHTML = '';
    
    // Agregar opción por defecto
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = placeholder;
    selectElement.appendChild(defaultOption);
    
    // Obtener y llenar roles
    return listarRolUsuario().then(data => {
        if (data.res && data.data) {
            data.data.forEach(rol => {
                const option = document.createElement('option');
                option.value = rol.rol;
                option.textContent = rol.rol.charAt(0).toUpperCase() + rol.rol.slice(1);
                selectElement.appendChild(option);
            });
        } else {
            console.error('No se pudieron cargar los roles:', data.msg);
        }
    });
}