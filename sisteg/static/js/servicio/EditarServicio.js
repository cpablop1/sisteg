import { cambiar } from './cambiar_mantenimiento.js';
import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';

export function editarServicio(id) {
    cambiar();
    
    // Cargar selects
    selectCliente();
    selectTipoPago();
    selectTipoServicio();
    selectRolUsuario();
    
    fetch(`/servicio/listar-servicios/?id=${id}`).then(res => res.json()).then(data => {
        if (data.res && data.data.length > 0) {
            let servicio = data.data[0];
            
            setTimeout(() => {
                // Llenar formulario
                document.getElementById('cliente_id').value = servicio.cliente_id || '';
                document.getElementById('tipo_pago_id').value = servicio.tipo_pago_id || '';
                document.getElementById('tipo_servicio_id').value = servicio.tipo_servicio_id || '';
                document.getElementById('rol_usuario_id').value = servicio.rol_usuario_id || '';
                document.getElementById('observacion').value = servicio.observacion || '';
                document.getElementById('costo_servicio').value = servicio.costo_servicio || '';
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
            }, 1000);
        }
    }).catch(error => {
        console.error('Error al cargar servicio:', error);
    });
}