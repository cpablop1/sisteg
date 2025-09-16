/**
 * Carga los usuarios con sus roles en un select.
 * 
 * Esta función obtiene los usuarios con roles asignados desde el servidor
 * y los carga en el elemento select con id 'rol_usuario_id'.
 * Muestra el formato: "Nombre Completo | Rol"
 * 
 * @example
 * // Cargar usuarios con roles en el select
 * selectRolUsuario();
 */
export function selectRolUsuario() {
    fetch('/autenticacion/listar-usuarios-con-roles/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('rol_usuario_id');
            if (select) {
                select.innerHTML = '';
                select.add(new Option('Seleccione técnico', ''));
                
                Array.from(data.data, item => {
                    // Formato: "Nombre Completo | Rol"
                    const displayText = `${item.nombre_completo} | ${item.rol}`;
                    select.add(new Option(displayText, item.usuario_id));
                });
            }
        } else {
            console.error('Error al cargar usuarios con roles:', data.msg);
        }
    }).catch(error => {
        console.error('Error de conexión al cargar usuarios con roles:', error);
    });
}