export function selectTipoServicio() {
    fetch('/servicio/listar-tipo-servicios/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('tipo_servicio_id');
            if (select) {
                select.innerHTML = '';
                select.add(new Option('Seleccione tipo de servicio', ''));
                Array.from(data.data, tipo => {
                    // Excluir venta (id = 1) para mantenimiento
                    if (tipo.id != 1) {
                        select.add(new Option(tipo.descripcion, tipo.id));
                    }
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar tipos de servicio:', error);
    });
}