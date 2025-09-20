import { cambiar } from './cambiar_mantenimiento.js';
import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';

export function editarServicio(id) {
    cambiar();
    
    // Cargar selects
    selectTipoPago();
    selectTipoServicio();
    
    // Cargar usuarios con roles y esperar a que se complete
    selectRolUsuario().then(() => {
        // Ahora cargar los datos del servicio
        fetch(`/servicio/listar-servicios/?id=${id}`).then(res => res.json()).then(data => {
            console.log('Datos recibidos del servidor:', data);
            if (data.res && data.data.length > 0) {
                let servicio = data.data[0];
                
                setTimeout(() => {
                    // Recargar select de cliente con el valor correcto
                    selectCliente(servicio.cliente_id);
                    
                    // Llenar otros campos del formulario
                    document.getElementById('tipo_pago_id').value = servicio.tipo_pago_id || '';
                    document.getElementById('tipo_servicio_id').value = servicio.tipo_servicio_id || '';
                    document.getElementById('rol_usuario_id').value = servicio.rol_usuario_id || '';
                    document.getElementById('observacion').value = servicio.observacion || '';
                    // El costo del servicio se maneja en la vista del técnico, no aquí
                    document.getElementById('subtotal').textContent = `Q. ${servicio.subtotal || '0.00'}`;
                    document.getElementById('ganancia').textContent = `Q. ${servicio.costo_servicio || '0.00'}`;
                    
                    // Mostrar botón de actualizar
                    document.getElementById('crear_servicio').hidden = true;
                    document.getElementById('actualizar_servicio').hidden = false;
                    document.getElementById('actualizar_servicio').setAttribute('servicio_id', id);
                    
                    // Cambiar título
                    let titulo = document.getElementById('titulo');
                    if (titulo) {
                        titulo.innerHTML = `<i class="fa-solid fa-wrench"></i> Editar Mantenimiento`;
                    }
                }, 500);
            }
        }).catch(error => {
            console.error('Error al cargar servicio:', error);
        });
    });
}