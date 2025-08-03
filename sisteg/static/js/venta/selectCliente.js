export function selectCliente() {
    fetch('/servicio/listar-cliente/?select=select').then(res => res.json()).then(data => {
        console.log(data);
        document.getElementById('cliente_id').innerHTML = '';
        Array.from(data.data, item => {
            document.getElementById('cliente_id').add(new Option(`${item.nombres} ${item.apellidos}`, item.id));
        });
    });
}