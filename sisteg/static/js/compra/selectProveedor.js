export function selectProveedor() {
    fetch('/compra/listar-proveedor/?select=select').then(res => res.json()).then(data => {
        document.getElementById('proveedor_id').innerHTML = '';
        console.log(data);
        Array.from(data.data, item => {
            document.getElementById('proveedor_id').add(new Option(`${item.nombres} ${item.apellidos}`, item.id));
        });
    });
}