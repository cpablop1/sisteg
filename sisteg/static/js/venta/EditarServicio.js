import { cambiar } from "./cambiar.js";
import { selectCliente } from "./selectCliente.js";

export function editarServicio(servicio_id) {
    console.log('Iniciando edición de servicio:', servicio_id);
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        console.log('Datos del servicio recibidos:', data);
        console.log('Cliente ID a seleccionar:', data.cliente_id);
        console.log('Tipo de cliente_id:', typeof data.cliente_id);
        console.log('Cliente_id es null?', data.cliente_id === null);
        console.log('Cliente_id es undefined?', data.cliente_id === undefined);
        
        // Cambiamos de vista primero, indicando que es modo edición
        cambiar(data.cliente_id);
        
        // Obtener buttons
        document.getElementById('confirmar_servicio').hidden = true;
        document.getElementById('crear_servicio').hidden = true;
        document.getElementById('eliminar_servicio').hidden = true;
        document.getElementById('actualizar_servicio').hidden = false;
        
        // Mostrar datos y recargar select con el cliente correcto
        setTimeout(() => {
            // Recargar select de cliente con el valor correcto
            selectCliente(data.cliente_id);
            
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            document.getElementById('tipo_servicio_id').value = data.tipo_servicio_id;
            document.getElementById('observacion').value = data.observacion;
            document.getElementById('rol_usuario_id').value = data.rol_usuario_id;
            document.getElementById('actualizar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
            
            // Verificar el estado del select después de un tiempo
            setTimeout(() => {
                const selectElement = document.getElementById('cliente_id');
                console.log('Valor del select después de la edición:', selectElement.value);
                console.log('Select2 está activo:', $(selectElement).hasClass('select2-hidden-accessible'));
            }, 1000);
        }, 200);
    });
}