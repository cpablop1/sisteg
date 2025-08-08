export function listarCarrito() {
    fetch(`/servicio/listar-carrito/`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar_carrito');
        let fila = '';
        if (data.data.length === 0) {
            let form_agregar = document.getElementById('form_agregar');
            form_agregar.reset();
            document.getElementById('subtotal').innerHTML = `Q 0.0`;
            document.getElementById('confirmar_servicio').removeAttribute('servicio_id');
            document.getElementById('eliminar_servicio').removeAttribute('servicio_id');
        } else {
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

            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('cliente_id').value = data.proveedor_id;
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            document.getElementById('eliminar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('confirmar_servicio').setAttribute('servicio_id', data.carrito_id);
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}