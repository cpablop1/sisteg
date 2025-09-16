export function selectTipoPago() {
    fetch('/inicio/listar-tipo-pago/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('tipo_pago_id');
            if (select) {
                select.innerHTML = '';
                select.add(new Option('Seleccione tipo de pago', ''));
                Array.from(data.data, tipo => {
                    select.add(new Option(tipo.descripcion, tipo.id));
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar tipos de pago:', error);
    });
}