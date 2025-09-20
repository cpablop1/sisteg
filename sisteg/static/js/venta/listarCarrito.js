export function listarCarrito(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar_carrito');
        let fila = '';
        console.log(data);
        console.log('Listando carrito...');
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
                        <th scope="row"><input type="number" class="form-control text-center" value="${elemento.cantidad}" producto_id="${elemento.producto_id}"></th>
                        <td>${elemento.producto}</td>
                        <td class="text-center">${elemento.precio}</td>
                        <td class="text-center">${elemento.total}</td>
                        <td class="text-center"><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}"></i></td>
                    </tr>`;
            });
            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            
            // Recargar select de cliente con el valor correcto
            if (data.cliente_id) {
                console.log('Recargando select de cliente con ID:', data.cliente_id);
                // Importar selectCliente dinámicamente
                import('./selectCliente.js').then(module => {
                    module.selectCliente(data.cliente_id);
                });
            }
            document.getElementById('eliminar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('confirmar_servicio').setAttribute('servicio_id', data.carrito_id);
            document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}