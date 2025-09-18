export function selectTipoPago() {
    fetch('/listar-tipo-pago/?select=select').then(res => res.json()).then(data => {
        console.log(data);
        if (data.res && data.data) {
            const select = document.getElementById('tipo_pago_id');
            if (select) {
                select.innerHTML = '';
                Array.from(data.data, tipo => {
                    select.add(new Option(tipo.descripcion, tipo.id));
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar tipos de pago:', error);
    });
}