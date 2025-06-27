export function listarCarrito() {
    fetch(`/compra/listar-carrito/`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar_carrito');
        let fila = '';
        console.log(data);
        Array.from(data.data, elemento => {
            fila += `
                <tr>
                    <th scope="row">${elemento.cantidad}</th>
                    <td>${elemento.producto}</td>
                    <td>${elemento.costo}</td>
                    <td>${elemento.total}</td>
                    <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" eliminar="${elemento.id}"></i></td>
                </tr>`;
        });

        tabla.childNodes[3].innerHTML = fila;
        document.getElementById('subtotal').innerHTML = data.subtotal;
        document.getElementById('proveedor_id').value = data.proveedor_id;
        document.getElementById('tipo_pago_id').value = data.tipo_pago_id;
    });
}