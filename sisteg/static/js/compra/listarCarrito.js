export function listarCarrito() {
    fetch(`/compra/listar-carrito/`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar_carrito');
        let fila = '';
        console.log(data.data.length);
        if (data.data.length === 0) {
            let form_agregar = document.getElementById('form_agregar');
            form_agregar.reset();
            document.getElementById('subtotal').innerHTML = `Q 0.0`;
        } else {
            Array.from(data.data, elemento => {
                fila += `
                    <tr>
                        <th scope="row">${elemento.cantidad}</th>
                        <td>${elemento.producto}</td>
                        <td>${elemento.costo}</td>
                        <td>${elemento.total}</td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_compra_id="${elemento.id}"></i></td>
                    </tr>`;
            });

            document.getElementById('subtotal').innerHTML = `Q ${data.subtotal}`;
            document.getElementById('proveedor_id').value = data.proveedor_id;
            document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
            document.getElementById('eliminar_compra').setAttribute('compra_id', data.carrito_id);
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}