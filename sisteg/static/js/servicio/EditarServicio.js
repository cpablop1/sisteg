import { cambiar } from "./cambiar.js";

export function editarServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        // Obtener inputs para rellenar
        let cliente_id = document.getElementById('cliente_id');
        let tipo_pago_id = document.getElementById('tipo_pago_id');
        let tipo_servicio_id = document.getElementById('tipo_servicio_id');
        let observacion = document.getElementById('observacion');
        let costo_servicio = document.getElementById('costo_servicio');
        let rol_usuario_id = document.getElementById('rol_usuario_id');
        let actualizar_servicio = document.getElementById('actualizar_servicio');
        let subtotal = document.getElementById('subtotal');
        console.log(data);
        // Mostar datos
        setTimeout(() => {
            cliente_id.value = data.cliente_id;
            tipo_pago_id.value = data.tipo_pago_id;
            tipo_servicio_id.value = data.tipo_servicio_id;
            observacion.value = data.observacion;
            costo_servicio.value = data.costo_servicio;
            rol_usuario_id.value = data.rol_usuario_id;
            subtotal.innerHTML = `Q ${data.subtotal}`;
            actualizar_servicio.setAttribute('servicio_id', data.carrito_id);
            // Listamos los detalles del servicio
            let tabla = document.getElementById('tbl_listar_carrito');
            let fila = '';
            if (data.data.length !== 0) {
                Array.from(data.data, elemento => {
                    fila += `
                    <tr>
                        <th scope="row"><input type="number" class="form-control" value="${elemento.cantidad}" producto_id="${elemento.producto_id}"></th>
                        <td>${elemento.producto}</td>
                        <td>${elemento.precio}</td>
                        <td>${elemento.total}</td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}"></i></td>
                    </tr>`;
                });
            }
            tabla.childNodes[3].innerHTML = fila;
        }, 500);
    });
}