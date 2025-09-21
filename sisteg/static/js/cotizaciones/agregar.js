import * as alerta from '../alertas/alertas.js';
import { listarCarrito } from './listarCarrito.js';

// Función para obtener el precio y costo de un producto desde la tabla de productos
function obtenerPrecioProducto(producto_id) {
    // Buscar el precio en la tabla de productos
    const filas = document.querySelectorAll('#tbl_listar_productos tbody tr');
    
    for (let fila of filas) {
        const agregarBtn = fila.querySelector('[agregar]');
        if (agregarBtn) {
            const btnProductoId = parseInt(agregarBtn.getAttribute('agregar'));
            
            if (btnProductoId === producto_id) {
                const precioCell = fila.querySelector('td:nth-child(3)'); // Columna de precio
                const costoCell = fila.querySelector('td:nth-child(4)'); // Columna de costo
                
                if (precioCell) {
                    const precio = parseFloat(precioCell.textContent.trim());
                    const costo = costoCell ? parseFloat(costoCell.textContent.trim()) : 0;
                    
                    return {
                        precio: precio,
                        costo: costo
                    };
                }
            }
        }
    }
    
    return null;
}

export function agregar(form, producto_id, cantidad) {
    let formData = new FormData(form);
    formData.append('producto_id', producto_id);
    formData.append('cantidad', cantidad);
    
    // Obtener servicio_id de manera más robusta
    let servicio_id = document.getElementById('confirmar_servicio').getAttribute('servicio_id') || 
                     document.getElementById('eliminar_servicio').getAttribute('servicio_id');
    
    if (servicio_id) {
        formData.append('servicio_id', servicio_id);
    }
    
    // Obtener precio y costo del producto desde la tabla de productos
    let datosProducto = obtenerPrecioProducto(producto_id);
    if (datosProducto) {
        formData.append('precio', datosProducto.precio);
        formData.append('costo', datosProducto.costo);
    }
    
    // Forzar tipo de servicio a venta (id = 1)
    formData.set('tipo_servicio_id', '1');
    
    fetch('/servicio/agregar-servicio/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    }).then(res => {
        return res.json();
    }).then(data => {
        if (data.res) {
            alerta.success(data.msg);
            listarCarrito();
        } else {
            alerta.danger(data.msg);
        }
    }).catch(error => {
        console.log(error);
    });
}