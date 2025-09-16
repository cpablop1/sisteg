export function selectCliente() {
    fetch('/servicio/listar-cliente/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('cliente_id');
            if (select) {
                select.innerHTML = '';
                select.add(new Option('Seleccione cliente', ''));
                Array.from(data.data, cliente => {
                    select.add(new Option(`${cliente.nombres} ${cliente.apellidos}`, cliente.id));
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar clientes:', error);
    });
}