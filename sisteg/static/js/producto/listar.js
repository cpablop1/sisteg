export function listar(data_p = { 'pagina': 1, 'buscar': '' }) {
    let params = new URLSearchParams(data_p).toString();
    fetch(`/producto/listar-producto/?${params}`).then(res => res.json()).then(data => {
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


        Array.from(data.data, (producto, indice) => {
            console.log(producto);
            fila += `
                <tr>
                    <th scope="row">${indice + 1}</th>
                    <td>${producto.descripcion}</td>
                    <td>${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.marca}</td>
                    <td>${producto.categoria}</td>
                    <td>${producto.usuario}</td>
                    <td>${producto.fecha_ingreso}</td>
                    <td>${producto.fecha_actualizacion}</td>
                    <td><i class="fa-solid fa-pen-to-square btn btn-warning btn-sm" editar="${producto.id}"></i></td>
                    <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" eliminar="${producto.id}"></i></td>
                </tr>`;
        });

        tabla.childNodes[3].innerHTML = fila;
        document.getElementById('pagination').innerHTML = previous + pages + next;
        document.getElementById(`page-${data_p.pagina}`).classList.add('active');
        document.getElementById('count').innerHTML = `Hay ${data.count} elementos contenidas en ${data.num_pages} páginas.`;

    });
}