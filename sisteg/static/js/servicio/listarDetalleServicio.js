export function listarDetalleServicio(servicio_id) {
    fetch(`/servicio/listar-carrito/?servicio_id=${servicio_id}`).then(res => res.json()).then(data => {
        if (data.res && data.data) {
            let tabla = document.getElementById('tbl_detalle_servicio');
            let fila = '';
            
            Array.from(data.data, (detalle, indice) => {
                fila += `
                    <tr>
                        <th scope="row">${indice + 1}</th>
                        <td>${detalle.producto}</td>
                        <td>Q. ${detalle.costo}</td>
                        <td>Q. ${detalle.precio}</td>
                        <td>${detalle.cantidad}</td>
                        <td>Q. ${detalle.total}</td>
                        <td>Q. ${detalle.ganancia}</td>
                    </tr>`;
            });
            
            tabla.childNodes[3].innerHTML = fila;
        }
    }).catch(error => {
        console.error('Error al cargar detalle del servicio:', error);
    });
}