import { cambiar } from './cambiar.js';
import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';

export function editarServicio(id) {
    // Cargar selects
    selectTipoPago();
    selectTipoServicio();

    // Cargar usuarios con roles y esperar a que se complete
    selectRolUsuario().then(() => {
        // Ahora cargar los datos del servicio
        fetch(`/servicio/listar-servicios/?id=${id}`).then(res => res.json()).then(data => {
            if (data.res && data.data.length > 0) {
                let servicio = data.data[0];

                setTimeout(() => {
                    // Recargar select de cliente con el valor correcto
                    selectCliente(servicio.cliente_id);
                    // Llenar otros campos del formulario
                    document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${servicio.telefono}` || '';
                    document.getElementById('tipo_pago_id').value = servicio.tipo_pago_id || '';
                    document.getElementById('tipo_servicio_id').value = servicio.tipo_servicio_id || '';
                    document.getElementById('rol_usuario_id').value = servicio.rol_usuario_id || '';
                    document.getElementById('observacion').value = servicio.observacion || '';
                    document.getElementById('nota').value = servicio.nota || '';
                    document.getElementById('subtotal').textContent = `Q. ${servicio.subtotal || '0.00'}`;
                    document.getElementById('ganancia').textContent = `Q. ${servicio.costo_servicio || '0.00'}`;

                    // Mostrar botón de actualizar
                    document.getElementById('crear_servicio').hidden = true;
                    document.getElementById('actualizar_servicio').hidden = false;
                    document.getElementById('actualizar_servicio').setAttribute('servicio_id', id);
                }, 500);
            }
        }).catch(error => {
            console.error('Error al cargar servicio:', error);
        });
    });
}