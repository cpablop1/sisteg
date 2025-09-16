import { cambiar } from "./cambiar.js";
import { llenarSelectRoles } from "./listarRolUsuario.js";

/**
 * Edita un usuario existente cargando sus datos en el formulario.
 * 
 * @param {number} id - ID del usuario a editar
 * 
 * @example
 * // Editar usuario con ID 1
 * editar(1);
 */
export function editar(id) {
    cambiar();
    
    // Cargar roles en el select
    const rolSelect = document.getElementById('rol');
    if (rolSelect) {
        llenarSelectRoles(rolSelect, 'Seleccione un rol');
    }
    
    fetch(`/autenticacion/listar-usuario/?id=${id}`).then(res => res.json()).then(data => {
        if (data.res && data.data.length > 0) {
            let usuario = data.data[0];
            let inputs = ['id', 'username', 'first_name', 'last_name', 'email'];
            
            setTimeout(() => {
                // Llenar campos básicos
                Array.from(inputs, value => {
                    const element = document.getElementById(value);
                    if (element) {
                        element.value = usuario[value] || '';
                    }
                });
                
                // Llenar campo de rol
                const rolSelect = document.getElementById('rol');
                if (rolSelect && usuario.rol) {
                    // Esperar a que se carguen los roles
                    setTimeout(() => {
                        rolSelect.value = usuario.rol;
                    }, 500);
                }
                
                // Cambiar el título del formulario
                const titulo = document.getElementById('titulo');
                if (titulo) {
                    titulo.innerHTML = `<i class="fa-solid fa-user-edit"></i> Editar Usuario`;
                }
                
            }, 1000);
        } else {
            console.error('Error al cargar datos del usuario:', data.msg);
        }
    }).catch(error => {
        console.error('Error de conexión:', error);
    });
}