import { cambiar } from './cambiar.js';
import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';

export function editarServicio(id) {
    // Cargar selects
    selectTipoPago();
    selectTipoServicio();

    // Cargar usuarios con roles y esperar a que se complete
    selectRolUsuario().then(() => {
        // Ahora cargar los datos del servicio
        fetch(`/servicio/listar-servicios/?id=${id}`).then(res => res.json()).then(data => {
            console.log(data)
            if (data.res && data.data.length > 0) {
                let servicio = data.data[0];
                setTimeout(() => {
                    // Recargar select de cliente con el valor correcto
                    selectCliente(servicio.cliente_id);
                    // Llenar otros campos del formulario
                    document.getElementById('telefono').innerHTML = `<b>Contacto:</b> ${servicio.telefono}` || '';
                    document.getElementById('tipo_pago_id').value = servicio.tipo_pago_id || '';
                    document.getElementById('tipo_servicio_id').value = servicio.tipo_servicio_id || '';
                    document.getElementById('rol_usuario_id').value = servicio.rol_usuario_id || '';
                    document.getElementById('observacion').value = servicio.observacion || '';
                    document.getElementById('nota').value = servicio.nota || '';
                    document.getElementById('subtotal').textContent = `Q. ${servicio.subtotal || '0.00'}`;
                    document.getElementById('ganancia').textContent = `Q. ${servicio.costo_servicio || '0.00'}`;

                    // Mostrar botón de actualizar
                    document.getElementById('crear_servicio').hidden = true;
                    document.getElementById('actualizar_servicio').hidden = false;
                    document.getElementById('actualizar_servicio').setAttribute('servicio_id', id);

                    // Listamos los detalles del servicio
                    let tabla = document.getElementById('tbl_listar_carrito');
                    let fila = '';
                    if (data.detalle_servicio.length !== 0) {
                        Array.from(data.detalle_servicio, elemento => {
                            fila += `
                    <tr>
                        <td scope="row"><input type="number" class="form-control" value="${elemento.cantidad}" producto_id="${elemento.producto_id}" id="cantidad${elemento.producto_id}"></td>
                        <td>${elemento.producto}</td>
                        <td><input type="number" step="0.1" value="${elemento.costo}" class="form-control" producto_id="${elemento.producto_id}" id="costo${elemento.producto_id}"></td>
                        <td><input type="number" step="0.1" value="${elemento.precio}" class="form-control" producto_id="${elemento.producto_id}" id="precio${elemento.producto_id}"></td>
                        <td>${elemento.total}</td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}"></i></td>
                    </tr>`;
                        });
                    }
                    tabla.childNodes[3].innerHTML = fila;
                }, 500);
            }
        }).catch(error => {
            console.error('Error al cargar servicio:', error);
        });
    });
}