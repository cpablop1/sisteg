export function listar(data_p = {'tipo_servicio': 'mantenimiento', 'pagina': 1, 'buscar': '' }) {
    let params = new URLSearchParams(data_p).toString();
    fetch(`/servicio/listar-servicios/?${params}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar');
        let fila = '';
        let pages = '';
        let previous;
        let next;
        if (data.has_next) {
            let new_data = { ...data_p }
            new_data.pagina += 1
            let jsonData = JSON.stringify(new_data);
            next = `<li class="page-item"><a class="page-link" href="#" onclick='listar(${jsonData})'><i class="fa-solid fa-circle-chevron-right"></i></a></li>`
        } else {
            next = `<li class="page-item disabled"><a class="page-link" href="#"><i class="fa-solid fa-circle-chevron-right"></i></a></li>`
        }
        if (data.has_previous) {
            let new_data = { ...data_p }
            new_data.pagina -= 1
            let jsonData = JSON.stringify(new_data);
            previous = `<li class="page-item"><a class="page-link" href="#" onclick='listar(${jsonData})'><i class="fa-solid fa-circle-chevron-left"></i></a></li>`
        } else {
            previous = `<li class="page-item disabled"><a class="page-link" href="#"><i class="fa-solid fa-circle-chevron-left"></i></a></li>`
        }
        Array.from(data.page_range, pagina => {
            let new_data = { ...data_p }
            new_data.pagina = pagina
            let jsonData = JSON.stringify(new_data);
            pages += `<li class="page-item" id="page-${pagina}"><a class="page-link" href="#" onclick='listar(${jsonData})'>${pagina}</a></li>`;
        });

        Array.from(data.data, (servicio, indice) => {
            let editar = '';
            let eliminar = '';
            let garantia = '';
            
            // Solo mostrar editar y eliminar si el servicio no está finalizado
            if (!servicio.estado_servicio) {
                editar = `<i class="fa-solid fa-pen-to-square btn btn-warning btn-sm" editar_servicio_id="${servicio.id}" title="Editar mantenimiento"></i>`;
                eliminar = `<i class="fa-solid fa-trash-can btn btn-danger btn-sm" eliminar_servicio_id="${servicio.id}" title="Eliminar mantenimiento"></i>`;
            }
            
            // Botón de garantía solo para servicios finalizados
            if (servicio.estado_servicio) {
                garantia = `<i class="fa-solid fa-shield-halved btn btn-info btn-sm" garantia_servicio servicio_id="${servicio.id}" garantia_id="0" title="Gestionar garantía"></i>`;
            }
            
            fila += `
                <tr>
                    <th scope="row">${indice + 1}</th>
                    <td>${servicio.cliente}</td>
                    <td>Q. ${servicio.subtotal}</td>
                    <td>${servicio.tipo_pago}</td>
                    <td>${servicio.usuario_id}</td>
                    <td>${servicio.tipo_servicio}</td>
                    <td>${servicio.tecnico}</td>
                    <td><span class="badge ${servicio.estado_servicio ? 'bg-success' : 'bg-warning'}">${servicio.estado}</span></td>
                    <td>${servicio.fecha_ingreso}</td>
                    <td>${servicio.fecha_actualizacion}</td>
                    <td><i class="fa-solid fa-circle-info btn btn-info btn-sm" servicio_id="${servicio.id}" title="Ver detalle"></i></td>
                    <td><i class="fa-solid fa-print btn btn-info btn-sm" ticket_servicio_id="${servicio.id}" title="Imprimir ticket"></i></td>
                    <td>${editar}</td>
                    <td>${eliminar}</td>
                </tr>`;
        });

        tabla.childNodes[3].innerHTML = fila;
        document.getElementById('pagination').innerHTML = previous + pages + next;
        document.getElementById(`page-${data_p.pagina}`).classList.add('active');
        document.getElementById('count').innerHTML = `Hay ${data.count} elementos contenidas en ${data.num_pages} páginas.`;

    });
}
