export function selectRolUsuario() {
    fetch('/autenticacion/listar-usuarios-con-roles/').then(res => res.json()).then(data => {
        if (data.res && data.data) {
            const select = document.getElementById('rol_usuario_id');
            if (select) {
                select.innerHTML = '';
                select.add(new Option('Seleccione técnico', ''));
                Array.from(data.data, item => {
                    const displayText = `${item.nombre_completo} | ${item.rol}`;
                    select.add(new Option(displayText, item.usuario_id));
                });
            }
        }
    }).catch(error => {
        console.error('Error al cargar usuarios con roles:', error);
    });
}