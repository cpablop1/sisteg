export function listarDetalleServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_detalle_servicio');
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
                        <td>${elemento.cantidad}</td>
                        <td>${elemento.producto}</td>
                        <td>${elemento.marca}</td>
                        <td>${elemento.precio}</td>
                        <td>${elemento.total}</td>
                    </tr>`;
            });
            document.getElementById('subtotal_detalle_servicio').innerHTML = `Q ${data.subtotal}`;
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}