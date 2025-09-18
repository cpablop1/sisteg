import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';
import { listar as listado } from './listar_mantenimiento.js';

// Función para cambiar de vista entre el formulario y el listado de mantenimiento
export function cambiar() {
    console.log('Ejecutando función cambiar() - Mantenimiento');
    
    // Obtener elementos del DOM con verificación robusta
    const btn_agregar = document.getElementById('agregar');
    const form_agregar = document.getElementById('form_agregar');
    const listar = document.getElementById('listar');
    const crear_servicio = document.getElementById('crear_servicio');
    const eliminar_servicio = document.getElementById('eliminar_servicio');
    const actualizar_servicio = document.getElementById('actualizar_servicio');

    // Verificar elementos críticos
    if (!btn_agregar) {
        console.error('Elemento "agregar" no encontrado');
        return;
    }
    if (!form_agregar) {
        console.error('Elemento "form_agregar" no encontrado');
        return;
    }
    if (!listar) {
        console.error('Elemento "listar" no encontrado');
        return;
    }

    // Resetear formulario
    try {
        const form_mantenimiento = document.getElementById('form_mantenimiento');
        if (form_mantenimiento) {
            form_mantenimiento.reset();
        }
    } catch (error) {
        console.error('Error al resetear formulario:', error);
    }

    // Limpiar atributo servicio_id si existe
    if (actualizar_servicio) {
        actualizar_servicio.removeAttribute('servicio_id');
        actualizar_servicio.hidden = true;
    }

    // Configurar botones con verificación
    if (crear_servicio) {
        crear_servicio.hidden = false;
    }
    if (eliminar_servicio) {
        eliminar_servicio.hidden = false;
    }

    // Alternar entre listado y formulario
    const estaOcultoListado = listar.style.display === 'none' || listar.hidden;
    
    if (estaOcultoListado) {
        // Mostrar listado, ocultar formulario
        console.log('Mostrando listado - Mantenimiento');
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        listar.style.display = 'block';
        listar.hidden = false;
        form_agregar.style.display = 'none';
        form_agregar.hidden = true;
        listado();
    } else {
        // Mostrar formulario, ocultar listado
        console.log('Mostrando formulario - Mantenimiento');
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        listar.style.display = 'none';
        listar.hidden = true;
        form_agregar.style.display = 'block';
        form_agregar.hidden = false;
        
        // Cargar datos para el formulario
        setTimeout(() => {
            selectCliente();
            selectTipoPago();
            selectTipoServicio();
            selectRolUsuario();
        }, 100);
    }
}
