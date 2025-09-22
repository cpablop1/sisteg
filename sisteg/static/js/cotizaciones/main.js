import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { validacion } from './validacion.js';
import { listarProductos } from './listarProductos.js';
import { eliminarServicio } from './eliminarServicio.js';
import { confirmarServicio } from './confirmarServicio.js';
import { listarDetalleServicio } from './listarDetalleServicio.js';
import { editarServicio } from './EditarServicio.js';
import { ticketPdf } from './ticketPdf.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { validacionCliente } from './validacionCliente.js';
import { agregarCliente } from './agregarCliente.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-money-check-dollar"></i> Cotizaciones`;
    listar();
}

window.listar = (data) => {
    listar(data);
}

window.listarProductos = (data) => {
    listarProductos(data);
}

// Evento para buscar productos
document.getElementById('buscar_productos').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listarProductos({ 'pagina': 1, 'buscar': buscar });
    } else {
        listarProductos();
    }
});

// Evento para cambiar de vista entre el carrito y el listado de servicios
document.getElementById('agregar').addEventListener('click', e => {
    cambiar();
});

// Evento para mostrar modal de buscar productos
document.getElementById('btn-buscar-productos').addEventListener('click', e => {
    new bootstrap.Modal(document.getElementById('mdl_buscar_productos')).show();
    setTimeout(() => listarProductos(), 500);
});

// Evento para agregar productos al carrito
document.getElementById('tbl_listar_productos').addEventListener('click', e => {
    let producto_id = parseInt(e.target.getAttribute('agregar'))
    let form = document.getElementById('form_agregar');

    if (producto_id) {
        if (validacion(form)) {
            agregar(form, producto_id);
        } else {
            alerta.warning('Complete el formulario para continuar.');
        }
    }
});

// Evento para buscar ventas
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({ 'cotiza': 1, 'pagina': 1, 'buscar': buscar });
    } else {
        listar();
    }
});

// Evento para eliminar elementos del servicio
document.getElementById('tbl_listar_carrito').addEventListener('click', e => {
    let detalle_servicio_id = parseInt(e.target.getAttribute('detalle_servicio_id'));
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    if (detalle_servicio_id) {
        eliminarServicio({ 'detalle_servicio_id': detalle_servicio_id });
        editarServicio(servicio_id);
    }
});

// Evento para eliminar el servicio completo
document.getElementById('eliminar_cotizacion').addEventListener('click', e => {
    let servicio_id = parseInt(document.getElementById('id').value);
    if (servicio_id) {
        eliminarServicio({ 'servicio_id': servicio_id });
        cambiar();
        listar();
    }
});

// Evento para crear una cotización
document.getElementById('crear_cotizacion').addEventListener('click', e => {
    let form = document.getElementById('form_agregar');

    if (validacion(form)) {
        agregar(form);
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }

})

// Evento para actualizar cantidad en carrito de servicio
document.getElementById('tbl_listar_carrito').addEventListener('keyup', e => {
    // Verificar que es un input de cantidad
    if (e.target.type !== 'number' || !e.target.hasAttribute('producto_id')) {
        return;
    }

    let form = document.getElementById('form_agregar');
    let cantidad = parseInt(e.target.value);
    let producto_id = parseInt(e.target.getAttribute('producto_id'));

    // Verificar que tenemos los datos necesarios
    if (!producto_id || isNaN(cantidad)) {
        return;
    }

    if (validacion(form)) {
        if (e.keyCode == 13) {
            if (cantidad > 0) {
                agregar(form, producto_id, cantidad);
            } else {
                alerta.danger('La cantidad debe ser mayor a 0.');
            }
        }
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para evetar el submit en formulario
document.getElementById('form_agregar').addEventListener('submit', e => {
    e.preventDefault();
});

// Evento para ver detalle de servicio
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    if (servicio_id) {
        new bootstrap.Modal(document.getElementById('mdl_detalle_servicio')).show();
        listarDetalleServicio(servicio_id);
    }
});

// Evento para visualizar servicio a editar
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('editar_servicio_id'));
    if (servicio_id) {
        editarServicio(servicio_id);
        cambiar();
    }
});

// Evento para editar servicio
document.getElementById('actualizar_cotizacion').addEventListener('click', e => {
    let form = document.getElementById('form_agregar');
    agregar(form);
});

// Evento para finalizar cotización
document.getElementById('finalizar_cotizacion').addEventListener('click', e => {
    let form = document.getElementById('form_agregar');
    let servicio_id = parseInt(document.getElementById('id').value.trim());
    let cliente_id = parseInt(document.getElementById('cliente_id').value);
    let tipo_pago_id = parseInt(document.getElementById('tipo_pago_id').value);

    if (servicio_id && validacion(form)){
        confirmarServicio({ servicio_id: servicio_id, cliente_id: cliente_id, tipo_pago_id: tipo_pago_id });
    } else{
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para imprimir ticket
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('ticket_servicio_id'));
    if (servicio_id) {
        ticketPdf(servicio_id);
    }
});

// Evento para mostrar modal de agregar cliente
document.getElementById('agregar_cliente').addEventListener('click', e => {
    new bootstrap.Modal(document.getElementById('mdl_agregar_cliente')).show();
});

// Evento para guardar cliente
document.getElementById('guardar_cliente').addEventListener('click', e => {
    let form = document.getElementById('form_agregar_cliente');
    if (validacionCliente(form)) {
        agregarCliente(form);
    }
});