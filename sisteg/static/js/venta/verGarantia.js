export function verGarantia(garantia_id) {
    fetch(`/servicio/listar-garantia/?garantia_id=${garantia_id}`).then(res => res.json()).then(data => {
        let form = document.getElementById('form_garantia');
        let select_producto = document.getElementById('detalle_servicio_id');
        select_producto.innerHTML = '';
        if (data.res) {
            console.log(data);
            // Mostramos los datos de la garantía
            form.elements['observacion'].value = data.observacion;
            form.elements['servicio_id'].value = data.servicio_id;
            data.perdida ? form.elements['es_perdida'].checked = true : form.elements['es_perdida'].checked = false;
            form.elements['garantia_id'].value = data.garantia_id;
            // Mostramos los detalles de garantía
            select_producto.add(new Option('------------------------', ''));
            if (data.ds.length != 0) {
                data.ds.forEach(ds => {
                    select_producto.add(new Option(ds.producto, ds.detalle_servicio_id));
                });
            }

            // Mostramos los detalles de la garantía
            let fila = '';
            if (data.dg.length != 0){
                data.dg.forEach(dg => {
                    fila += `<tr>
                                <td>${dg.cantidad}</td>
                                <td>${dg.producto}</td>
                                <td>${dg.marca}</td>
                                <td>${dg.precio}</td>
                                <td>${dg.costo}</td>
                                <td>${dg.total}</td>
                            </tr>`;
                });
            }
            document.getElementById('tbl_garantia').childNodes[3].innerHTML = fila;
        }
    });
}