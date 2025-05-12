export function listar() {
    fetch('/producto/listar-categoria/').then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar');
        let fila = '';
        Array.from(data.data, (item, index) => {
            fila += `
                <tr>
                    <th scope="row">${index + 1}</th>
                    <td>${item.descripcion}</td>
                    <td>${item.usuario}</td>
                    <td>${item.fecha_ingreso}</td>
                    <td>${item.fecha_actualizacion}</td>
                    <td><i class="fa-solid fa-pen-to-square btn btn-warning btn-sm" editar="${item.id}"></i></td>
                    <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" eliminar="${item.id}"></i></td>
                </tr>`;
        });

        tabla.childNodes[3].innerHTML = fila;
    });
}