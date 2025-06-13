export function selectCategoria() {
    fetch('/producto/listar-categoria?select=select').then(res => res.json()).then(data => {
        document.getElementById('categoria_id').innerHTML = '';
        Array.from(data.data, item => {
            document.getElementById('categoria_id').add(new Option(item.descripcion, item.id));
        });
    });
}