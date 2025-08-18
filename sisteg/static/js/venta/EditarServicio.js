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
        // Obtener inputs para rellenar
        let cliente_id = document.getElementById('cliente_id');
        let tipo_pago_id = document.getElementById('tipo_pago_id');
        let tipo_servicio_id = document.getElementById('tipo_servicio_id');
        let observacion = document.getElementById('observacion');
        let rol_usuario_id = document.getElementById('rol_usuario_id');
        let subtotal = document.getElementById('subtotal');
        // Mostar datos
        setTimeout(() => {
            cliente_id.value = data.cliente_id;
            tipo_pago_id.value = data.tipo_pago_id;
            tipo_servicio_id.value = data.tipo_servicio_id;
            observacion.value = data.observacion;
            rol_usuario_id.value = data.rol_usuario_id;
        }, 500);
        console.log(data);
    });
}