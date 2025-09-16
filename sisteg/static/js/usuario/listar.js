/**
 * Lista usuarios con paginación y búsqueda.
 * 
 * @param {Object} data_p - Parámetros de paginación y búsqueda
 * @param {number} data_p.pagina - Número de página actual
 * @param {string} data_p.buscar - Término de búsqueda
 * 
 * @example
 * // Listar primera página
 * listar({ 'pagina': 1, 'buscar': '' });
 * 
 * // Buscar usuarios
 * listar({ 'pagina': 1, 'buscar': 'admin' });
 */
export function listar(data_p = { 'pagina': 1, 'buscar': '' }) {
    let params = new URLSearchParams(data_p).toString();
    fetch(`/autenticacion/listar-usuario/?${params}`).then(res => res.json()).then(data => {
        let tabla = document.getElementById('tbl_listar');
        let fila = '';
        let pages = '';
        let previous;
        let next;
        
        // Generar botón siguiente
        if (data.has_next) {
            let new_data = { ...data_p }
            new_data.pagina += 1
            let jsonData = JSON.stringify(new_data);
            next = `<li class="page-item"><a class="page-link" href="#" onclick='listar(${jsonData})'><i class="fa-solid fa-circle-chevron-right"></i></a></li>`
        } else {
            next = `<li class="page-item disabled"><a class="page-link" href="#"><i class="fa-solid fa-circle-chevron-right"></i></a></li>`
        }
        
        // Generar botón anterior
        if (data.has_previous) {
            let new_data = { ...data_p }
            new_data.pagina -= 1
            let jsonData = JSON.stringify(new_data);
            previous = `<li class="page-item"><a class="page-link" href="#" onclick='listar(${jsonData})'><i class="fa-solid fa-circle-chevron-left"></i></a></li>`
        } else {
            previous = `<li class="page-item disabled"><a class="page-link" href="#"><i class="fa-solid fa-circle-chevron-left"></i></a></li>`
        }
        
        // Generar números de página
        Array.from(data.page_range, pagina => {
            let new_data = { ...data_p }
            new_data.pagina = pagina
            let jsonData = JSON.stringify(new_data);
            pages += `<li class="page-item" id="page-${pagina}"><a class="page-link" href="#" onclick='listar(${jsonData})'>${pagina}</a></li>`;
        });

        // Generar filas de la tabla
        Array.from(data.data, (usuario, indice) => {
            // Formatear fechas
            const fechaRegistro = usuario.date_joined ? new Date(usuario.date_joined).toLocaleDateString('es-ES') : 'N/A';
            const ultimoAcceso = usuario.last_login ? new Date(usuario.last_login).toLocaleDateString('es-ES') : 'Nunca';
            
            // Determinar estado del usuario
            const estado = usuario.is_active ? 
                '<span class="badge bg-success">Activo</span>' : 
                '<span class="badge bg-danger">Inactivo</span>';
            
            // Determinar si es admin
            const esAdmin = usuario.is_superuser ? 
                '<span class="badge bg-primary">Sí</span>' : 
                '<span class="badge bg-secondary">No</span>';
            
            // Capitalizar rol
            const rol = usuario.rol ? 
                usuario.rol.charAt(0).toUpperCase() + usuario.rol.slice(1) : 
                'Sin rol';

            fila += `
                <tr>
                    <th scope="row">${indice + 1}</th>
                    <td>${usuario.username}</td>
                    <td>${usuario.first_name || 'N/A'}</td>
                    <td>${usuario.last_name || 'N/A'}</td>
                    <td>${usuario.email || 'N/A'}</td>
                    <td>${rol}</td>
                    <td>${estado}</td>
                    <td>${esAdmin}</td>
                    <td>${ultimoAcceso}</td>
                    <td>${fechaRegistro}</td>
                    <td><i class="fa-solid fa-pen-to-square btn btn-warning btn-sm" editar="${usuario.id}" title="Editar usuario"></i></td>
                </tr>`;
        });

        // Actualizar tabla y paginación
        tabla.childNodes[3].innerHTML = fila;
        document.getElementById('pagination').innerHTML = previous + pages + next;
        
        // Marcar página activa
        if (document.getElementById(`page-${data_p.pagina}`)) {
            document.getElementById(`page-${data_p.pagina}`).classList.add('active');
        }
        
        // Actualizar contador
        document.getElementById('count').innerHTML = `Hay ${data.count} usuarios en ${data.num_pages} páginas.`;

    }).catch(error => {
        console.error('Error al cargar usuarios:', error);
        document.getElementById('tbl_listar').childNodes[3].innerHTML = 
            '<tr><td colspan="11" class="text-center text-danger">Error al cargar los datos</td></tr>';
    });
}