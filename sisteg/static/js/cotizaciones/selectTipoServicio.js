export function selectTipoServicio() {
    fetch('/servicio/listar-tipo-servicios/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('tipo_servicio_id');
            if (select) {
                select.innerHTML = '';
                Array.from(data.data, tipo => {
                    select.add(new Option(tipo.descripcion, tipo.id));
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar tipos de servicio:', error);
    });
}