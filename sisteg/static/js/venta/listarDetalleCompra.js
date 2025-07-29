export function listarDetalleCompra(compra_id) {
    fetch(`/compra/listar-carrito/?compra_id=${compra_id}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_detalle_compra');
        let fila = '';
        if (data.data.length === 0) {
            let form_agregar = document.getElementById('form_agregar');
            form_agregar.reset();
            document.getElementById('subtotal').innerHTML = `Q 0.0`;
            document.getElementById('confirmar_compra').removeAttribute('compra_id');
            document.getElementById('eliminar_compra').removeAttribute('compra_id');
        } else {
            Array.from(data.data, elemento => {
                fila += `
                    <tr>
                        <td>${elemento.cantidad}</td>
                        <td>${elemento.producto}</td>
                        <td>${elemento.marca}</td>
                        <td>${elemento.costo}</td>
                        <td>${elemento.total}</td>
                    </tr>`;
            });
            document.getElementById('subtotal_detalle_compra').innerHTML = `Q ${data.subtotal}`;
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}