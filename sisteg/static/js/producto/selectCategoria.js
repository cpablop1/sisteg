export function selectCategoria() {
    fetch('/producto/listar-categoria/').then(res => res.json()).then(data => {
        document.getElementById('categoria_id').innerHTML = '';
        document.getElementById('categoria_id').add(new Option('Seleccione la categoría', ''));
        Array.from(data.data, item => {
            document.getElementById('categoria_id').add(new Option(item.descripcion, item.id));
        });
    });
}