export function selectTipoPago() {
    fetch('/listar-tipo-pago/?select=select').then(res => res.json()).then(data => {
        document.getElementById('tipo_pago_id').innerHTML = '';
        Array.from(data.data, item => {
            document.getElementById('tipo_pago_id').add(new Option(item.descripcion, item.id));
        });
    });
}