export function selectTipoServicio() {
    fetch('/servicio/listar-tipo-servicios/').then(res => res.json()).then(data => {
        document.getElementById('tipo_servicio_id').innerHTML = '';
        Array.from(data.data, item => {
            document.getElementById('tipo_servicio_id').add(new Option(item.descripcion, item.id));
        });
    });
}