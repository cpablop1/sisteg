export function verGarantia(garantia_id) {
    fetch(`/servicio/listar-garantia/?garantia_id=${garantia_id}`).then(res => res.json()).then(data => {
        let form = document.getElementById('form_garantia');
        if (data.res) {
            console.log(data);
            form.elements['observacion'].value = data.observacion;
            form.elements['servicio_id'].value = data.servicio_id;
            data.perdida ? form.elements['es_perdida'].checked = true : form.elements['es_perdida'].checked = false;
            form.elements['garantia_id'].value = data.garantia_id;
        }
    });
}