export function editarServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        // Mostar datos despues de 500 milisegundos
        setTimeout(() => {
            document.getElementById('cliente_id').value = data.cliente_id;
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            document.getElementById('tipo_servicio_id').value = data.tipo_servicio_id;
            document.getElementById('observacion').value = data.observacion;
            document.getElementById('costo_servicio').value = data.costo_servicio;
            document.getElementById('rol_usuario_id').value = data.rol_usuario_id;
            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('actualizar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('finalizar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
            // Listamos los detalles del servicio
            let tabla = document.getElementById('tbl_listar_carrito');
            let fila = '';
            if (data.data.length !== 0) {
                Array.from(data.data, elemento => {
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
                    <tr class="text-center">
                        <td scope="row"><input type="number" class="form-control text-center" value="${elemento.cantidad}" id="cantidad${elemento.producto_id}"></td>
                        <td>${elemento.producto}</td>
                        <td>${stock}</td>
                        <td><input type="number" step="0.1" value="${elemento.costo}" class="form-control text-center" id="costo${elemento.producto_id}"></td>
                        <td><input type="number" step="0.1" value="${elemento.precio}" class="form-control text-center" id="precio${elemento.producto_id}"></td>
                        <td>${elemento.total}</td>
                        <td><i class="fa-solid fa-arrow-rotate-right btn btn-info" producto_id="${elemento.producto_id}"></i></td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}"></i></td>
                    </tr>`;
                });
            }
            tabla.childNodes[3].innerHTML = fila;
        }, 500);
    });
}