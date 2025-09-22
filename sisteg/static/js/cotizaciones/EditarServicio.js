import { cambiar } from "./cambiar.js";
import { selectCliente } from "./selectCliente.js";
import { selectRolUsuario } from "./selectRolUsuario.js";

export function editarServicio(servicio_id) {
    fetch(`/servicio/listar-servicios/?id=${servicio_id}`).then(res => res.json()).then(data => {
        // Cambiamos de vista primero, indicando que es modo edición
        //cambiar(data.cliente_id);
        // Obtener buttons
        console.log(data);
        let tabla = document.getElementById('tbl_listar_carrito');
        let fila = '';
        document.getElementById('crear_cotizacion').hidden = true;
        document.getElementById('eliminar_cotizacion').hidden = false;
        document.getElementById('actualizar_cotizacion').hidden = false;
        document.getElementById('finalizar_cotizacion').hidden = false;

        // Mostrar datos y recargar select con el cliente correcto
        setTimeout(() => {
            // Recargar select de cliente con el valor correcto
            selectCliente(data.data[0].cliente_id);

            document.getElementById('tipo_pago_id').value = data.data[0].tipo_pago_id;
            document.getElementById('tipo_servicio_id').value = data.data[0].tipo_servicio_id;
            document.getElementById('observacion').value = data.data[0].observacion;
            document.getElementById('rol_usuario_id').value = data.data[0].rol_usuario_id;
            document.getElementById('actualizar_cotizacion').setAttribute('servicio_id', data.data[0].id);
            document.getElementById('subtotal').innerHTML = `Q ${data.data[0].subtotal}`;
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.data[0].telefono}`;
            document.getElementById('id').value = data.data[0].id;

            if (data.detalle_servicio.length != 0) {
                Array.from(data.detalle_servicio, elemento => {
                    fila += `
                    <tr>
                        <th scope="row"><input type="number" class="form-control text-center" value="${elemento.cantidad}" producto_id="${elemento.producto_id}"></th>
                        <td>${elemento.producto}</td>
                        <td class="text-center">${elemento.precio}</td>
                        <td class="text-center">${elemento.total}</td>
                        <td class="text-center"><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}" servicio_id="${data.data[0].id}"></i></td>
                    </tr>`;
                });
            }
            tabla.childNodes[3].innerHTML = fila;
        }, 500);
    });
}