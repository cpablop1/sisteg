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
            if (data.res && data.data.length > 0) {
                let servicio = data.data[0];
                console.log(data)
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
                    document.getElementById('costo_servicio').value = servicio.costo_servicio || '';

                    // Mostrar botón de actualizar
                    document.getElementById('crear_servicio').hidden = true;
                    document.getElementById('actualizar_servicio').hidden = false;
                    document.getElementById('actualizar_servicio').setAttribute('servicio_id', id);

                    // Listamos los detalles del servicio
                    let tabla = document.getElementById('tbl_listar_carrito');
                    let fila = '';
                    if (data.detalle_servicio.length !== 0) {
                        Array.from(data.detalle_servicio, elemento => {
                            let stock = '';
                            if (elemento.stock) {
                                stock = `<div class="form-check text-center">
                                    <input class="form-check-input" type="checkbox" id="stock${elemento.producto_id}" checked>
                                    <label class="form-check-label" for="stock">Descontar</label>
                                </div>`;
                            } else {
                                stock = `<div class="form-check text-center">
                                    <input class="form-check-input" type="checkbox" id="stock${elemento.producto_id}">
                                    <label class="form-check-label" for="stock">No descontar</label>
                                </div>`;
                            }
                            fila += `
                    <tr class="text-center">
                        <td scope="row"><input type="number" class="form-control text-center" value="${elemento.cantidad}" id="cantidad${elemento.producto_id}"></td>
                        <td>${elemento.producto}</td>
                        <td>${stock}</td>
                        <td><input type="number" step="0.1" value="${elemento.costo}" class="form-control text-center" id="costo${elemento.producto_id}"></td>
                        <td><input type="number" step="0.1" value="${elemento.precio}" class="form-control text-center" id="precio${elemento.producto_id}"></td>
                        <td>${elemento.total}</td>
                        <td><i class="fa-solid fa-arrow-rotate-right btn btn-info" producto_id="${elemento.producto_id}"></i></td>
                        <td><i class="fa-solid fa-trash-can btn btn-danger btn-sm" detalle_servicio_id="${elemento.id}" servicio_id="${id}"></i></td>
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