export function listarDetalleServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_detalle_servicio');
        let fila = '';
        let garantia_servicio = document.getElementById('garantia_servicio');
        console.log(data);
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
        document.getElementById('descripcion').innerHTML = `<b>Descripción:</b> ${data.observacion}`;
        document.getElementById('cliente').innerHTML = `<b>Cliente:</b> ${data.cliente}`;
        document.getElementById('contacto').innerHTML = `<b>Contacto:</b> ${data.contacto}`;
        document.getElementById('mano_obra').innerHTML = `<b>Mano de obra:</b> Q ${data.costo_servicio}`;
        garantia_servicio.setAttribute('servicio_id', data.carrito_id);
        if (data.garantia_id) {
            garantia_servicio.classList.remove('btn-warning');
            garantia_servicio.classList.add('btn-info');
            garantia_servicio.setAttribute('garantia_id', data.garantia_id);
            garantia_servicio.innerHTML = `<i class="fa-solid fa-eye"></i> Ver garantía`;
        } else {
            garantia_servicio.classList.remove('btn-info')
            garantia_servicio.classList.add('btn-warning')
            garantia_servicio.removeAttribute('garantia_id')
            garantia_servicio.innerHTML = `<i class="fa-solid fa-square-plus"></i> Agregar garantía`;
        }
        tabla.childNodes[3].innerHTML = fila;
    });
}