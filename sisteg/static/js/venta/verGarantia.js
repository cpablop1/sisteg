export function verGarantia(garantia_id) {
    fetch(`/servicio/listar-garantia/?garantia_id=${garantia_id}`).then(res => res.json()).then(data => {
        let form = document.getElementById('form_garantia');
        let select_producto = document.getElementById('detalle_servicio_id');
        form.reset();
        select_producto.innerHTML = '';
        if (data.res) {
            console.log(data);
            // Mostramos los datos de la garantía
            form.elements['observacion'].value = data.observacion;
            form.elements['servicio_id'].value = data.servicio_id;
            data.perdida ? form.elements['es_perdida'].checked = true : form.elements['es_perdida'].checked = false;
            form.elements['garantia_id'].value = data.garantia_id;
            document.getElementById('subtotal_garantia').innerHTML = `Q ${data.subtotal}`;
            // Mostramos los detalles de garantía
            select_producto.add(new Option('------------------------', ''));
            if (data.ds.length != 0) {
                data.ds.forEach(ds => {
                    select_producto.add(new Option(ds.producto, ds.detalle_servicio_id));
                });
            }

            // Mostramos los detalles de la garantía
            let fila = '';
            if (data.dg.length != 0) {
                data.dg.forEach(dg => {
                    fila += `<tr class="text-center">
                                <td>${dg.cantidad}</td>
                                <td>${dg.producto}</td>
                                <td>${dg.marca}</td>
                                <td>${dg.precio}</td>
                                <td>${dg.costo}</td>
                                <td>${dg.total}</td>
                                <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" garantia_id="${garantia_id}" detalle_garantia_id="${dg.detalle_garantia_id}"></i></td>
                            </tr>`;
                });
            }
            let crear_garantia = document.getElementById('crear_garantia');
            if (data.garantia_id) {
                crear_garantia.innerHTML = '<i class="fa-solid fa-arrow-rotate-left"></i> Actualizar';
                crear_garantia.classList.remove('btn-primary');
                crear_garantia.classList.add('btn-warning');
            } else {
                crear_garantia.innerHTML = '<i class="fa-solid fa-square-plus"></i> Crear';
                crear_garantia.classList.remove('btn-warning');
                crear_garantia.classList.add('btn-primary');
            }
            document.getElementById('tbl_garantia').childNodes[3].innerHTML = fila;
        }
    });
}