import { cambiar } from "./cambiar.js";
import { selectCliente } from "./selectCliente.js";
import { selectRolUsuario } from "./selectRolUsuario.js";

export function editarServicio(servicio_id) {
    fetch(`/servicio/listar-servicios/?id=${servicio_id}`).then(res => res.json()).then(data => {
        // Obtener buttons
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
            document.getElementById('nota').value = data.data[0].nota;
            document.getElementById('rol_usuario_id').value = data.data[0].rol_usuario_id;
            document.getElementById('actualizar_cotizacion').setAttribute('servicio_id', data.data[0].id);
            document.getElementById('subtotal').innerHTML = `Q ${data.data[0].subtotal}`;
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.data[0].telefono}`;
            document.getElementById('costo_servicio').value = data.data[0].costo_servicio;
            document.getElementById('id').value = data.data[0].id;

            if (data.detalle_servicio.length != 0) {
                Array.from(data.detalle_servicio, elemento => {
                    let stock = '';
                    if (elemento.stock) {
                        stock = `<div class="form-check text-center">
                                    <input class="form-check-input" type="checkbox" id="stock${elemento.producto_id}" checked>
                                    <label class="form-check-label" for="stock">Descontar</label>
                                </div>`;
                    } else {
                        stock = `<div class="form-check text-center">
                                    <input class="form-check-input" type="checkbox" id="stock${elemento.producto_id}">
                                    <label class="form-check-label" for="stock">No descontar</label>
                                </div>`;
                    }
                    fila += `
                    <tr>
                        <th scope="row"><input type="number" class="form-control text-center" value="${elemento.cantidad}" id="cantidad${elemento.producto_id}"></th>
                        <td>${elemento.producto}</td>
                        <td ${hidden}>${stock}</td>
                        <td><input type="number" step="0.1" value="${elemento.costo}" class="form-control text-center" id="costo${elemento.producto_id}" ${rol}></td>
                        <td><input type="number" step="0.1" value="${elemento.precio}" class="form-control text-center" id="precio${elemento.producto_id}" ${rol}></td>
                        <td class="text-center">${elemento.total}</td>
                        <td><i class="fa-solid fa-arrow-rotate-right btn btn-info" producto_id="${elemento.producto_id}"></i></td>
                        <td class="text-center"><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}" servicio_id="${data.data[0].id}"></i></td>
                    </tr>`;
                });
            }
            tabla.childNodes[3].innerHTML = fila;
        }, 500);
    });
}