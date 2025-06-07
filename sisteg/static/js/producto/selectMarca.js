export function selectMarca() {
    fetch('/producto/listar-marca/').then(res => res.json()).then(data => {
        document.getElementById('marca_id').innerHTML = '';
        document.getElementById('marca_id').add(new Option('Seleccione la marca', ''));
        Array.from(data.data, item => {
            document.getElementById('marca_id').add(new Option(item.descripcion, item.id));
        });
    });
}