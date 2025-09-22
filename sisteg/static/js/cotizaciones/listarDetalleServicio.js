export function listarDetalleServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_detalle_servicio');
        let fila = '';
        if (data.data.length !== 0) {
            Array.from(data.data, elemento => {
                fila += `
                    <tr>
                        <td class="text-center">${elemento.cantidad}</td>
                        <td>${elemento.producto}</td>
                        <td>${elemento.marca}</td>
                        <td class="text-center">${elemento.precio}</td>
                        <td class="text-center">${elemento.costo}</td>
                        <td class="text-center">${elemento.ganancia}</td>
                        <td class="text-center">${elemento.total}</td>
                    </tr>`;
            });
        }
        document.getElementById('subtotal_detalle_servicio').innerHTML = `Subtotal Q ${data.subtotal}`;
        document.getElementById('ganancia_detalle_servicio').innerHTML = `Ganancia Q ${data.ganancia}`;
        document.getElementById('cliente').innerHTML = `<b>Cliente:</b> ${data.cliente}`;
        document.getElementById('contacto').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
        tabla.childNodes[3].innerHTML = fila;
    });
}