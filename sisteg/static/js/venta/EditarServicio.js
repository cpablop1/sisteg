import { cambiar } from "./cambiar.js";

export function editarServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        // Cambiamos de vista
        cambiar();
        // Obtener buttons
        document.getElementById('confirmar_servicio').hidden = true;
        document.getElementById('crear_servicio').hidden = true;
        document.getElementById('eliminar_servicio').hidden = true;
        document.getElementById('actualizar_servicio').hidden = false;
        // Mostar datos
        setTimeout(() => {
            document.getElementById('cliente_id').value = data.cliente_id;
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            document.getElementById('tipo_servicio_id').value = data.tipo_servicio_id;
            document.getElementById('observacion').value = data.observacion;
            document.getElementById('rol_usuario_id').value = data.rol_usuario_id;
            document.getElementById('actualizar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
        }, 500);
    });
}