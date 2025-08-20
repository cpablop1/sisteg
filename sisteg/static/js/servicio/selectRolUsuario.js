export function selectRolUsuario() {
    fetch('/autenticacion/listar-rol-usuario/').then(res => res.json()).then(data => {
        document.getElementById('rol_usuario_id').innerHTML = '';
        document.getElementById('rol_usuario_id').add(new Option('Seleccione ténico', ''));
        Array.from(data.data, item => {
            document.getElementById('rol_usuario_id').add(new Option(`${item.rol} | ${item.usuario}`, item.usuario_id));
        });
    });
}