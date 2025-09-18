export function verGarantia(garantia_id) {
    fetch(`/servicio/listar-garantia/?garantia_id=${garantia_id}`).then(res => res.json()).then(data => {
        if (data.res) {
            // Llenar formulario
            document.getElementById('servicio_id').value = data.servicio_id;
            document.getElementById('garantia_id').value = data.garantia_id;
            document.getElementById('observacion').value = data.observacion;
            document.getElementById('es_perdida').checked = data.perdida;
            
            // Llenar tabla de garantía
            let tabla = document.getElementById('tbl_garantia');
            let fila = '';
            
            Array.from(data.dg, (detalle, indice) => {
                fila += `
                    <tr>
                        <th scope="row">${indice + 1}</th>
                        <td>${detalle.producto}</td>
                        <td>${detalle.marca}</td>
                        <td>${detalle.cantidad}</td>
                        <td>Q. ${detalle.precio}</td>
                        <td>Q. ${detalle.total}</td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_garantia_id="${detalle.detalle_garantia_id}" garantia_id="${detalle.garantia_id}" title="Eliminar"></i></td>
                    </tr>`;
            });
            
            tabla.childNodes[3].innerHTML = fila;
            
            // Cambiar botón
            let crear_garantia = document.getElementById('crear_garantia');
            crear_garantia.innerHTML = '<i class="fa-solid fa-square-check"></i> Actualizar';
            crear_garantia.classList.remove('btn-primary');
            crear_garantia.classList.add('btn-warning');
        }
    }).catch(error => {
        console.error('Error al cargar garantía:', error);
    });
}

