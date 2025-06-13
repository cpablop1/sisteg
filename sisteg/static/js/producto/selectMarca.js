export function selectMarca() {
    fetch('/producto/listar-marca?select=select').then(res => res.json()).then(data => {
        document.getElementById('marca_id').innerHTML = '';
        Array.from(data.data, item => {
            document.getElementById('marca_id').add(new Option(item.descripcion, item.id));
        });
    });
}