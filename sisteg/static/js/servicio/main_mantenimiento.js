import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar_mantenimiento.js';
import { agregar, actualizar } from './agregar_mantenimiento.js';
import { listar } from './listar_mantenimiento.js';
import { validacion } from './validacion_mantenimiento.js';
import { eliminarServicio } from './eliminarServicio.js';
import { listarDetalleServicio } from './listarDetalleServicio.js';
import { editarServicio } from './EditarServicio.js';
import { ticketPdf } from './ticketPdf.js';
import { garantiaServicio } from './garantiaServicio.js';
import { verGarantia } from './verGarantia.js';
import { eliminarGarantia } from './eliminarGarantia.js';
import { selectCliente } from './selectCliente.js';
import { selectTipoPago } from './selectTipoPago.js';
import { selectTipoServicio } from './selectTipoServicio.js';
import { selectRolUsuario } from './selectRolUsuario.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-wrench"></i> Mantenimiento`;
    listar();
}

window.listar = (data) => {
    listar(data);
}

// Evento para cambiar de vista entre el formulario y el listado
document.getElementById('agregar').addEventListener('click', e => {
    cambiar();
    // Cargar selects necesarios
    selectCliente();
    selectTipoPago();
    selectTipoServicio();
    selectRolUsuario();
});

// Evento para buscar servicios de mantenimiento
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({ 'tipo_servicio': 'mantenimiento', 'pagina': 1, 'buscar': buscar });
    } else {
        listar();
    }
});

// Evento para eliminar el servicio completo
document.getElementById('eliminar_servicio').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    if (servicio_id) {
        eliminarServicio({ 'servicio_id': servicio_id });
    }
});

// Evento para evetar el submit en formulario
document.getElementById('form_mantenimiento').addEventListener('submit', e => {
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

// Evento para crear servicio de mantenimiento
document.getElementById('crear_servicio').addEventListener('click', e => {
    let form = document.getElementById('form_mantenimiento');

    if (validacion(form)) {
        agregar(form);
    } else {
        alerta.warning('Complete el formulario para continuar.');
    }
});

// Evento para editar servicio
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('editar_servicio_id'));
    if (servicio_id) {
        editarServicio(servicio_id);
    }
});

// Evento para actualizar servicio
document.getElementById('actualizar_servicio').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    let form = document.getElementById('form_mantenimiento');
    if (servicio_id) {
        console.log(servicio_id);
        actualizar(form, servicio_id);
        cambiar();
        setTimeout(() => {
            listar();
        }, 500);
    }
});

// Evento para eliminar el servicio tipo mantenimiento
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('eliminar_servicio_id'));
    if (servicio_id) {
        eliminarServicio({ 'servicio_id': servicio_id });
        setTimeout(() => {
            listar();
        }, 500);
    }
});

// Evento para imprimir ticket
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('ticket_servicio_id'));
    if (servicio_id) {
        ticketPdf(servicio_id);
    }
});

// Evento para mostra modal de garantía (usando event delegation)
document.addEventListener('click', e => {
    if (e.target.hasAttribute('garantia_servicio')) {
        let servicio_id = parseInt(e.target.getAttribute('servicio_id'))
        let garantia_id = parseInt(e.target.getAttribute('garantia_id'))
        document.getElementById('form_garantia').reset();
        if (servicio_id) {
            new bootstrap.Modal(document.getElementById('mdl_garantia')).show();
            if (garantia_id) {
                setTimeout(() => verGarantia(garantia_id), 500);
            } else {
                let crear_garantia = document.getElementById('crear_garantia');
                crear_garantia.innerHTML = '<i class="fa-solid fa-square-plus"></i> Crear';
                crear_garantia.classList.remove('btn-warning');
                crear_garantia.classList.add('btn-primary');
            }
        }
    }
});

// Evento para agregar garantía
document.getElementById('crear_garantia').addEventListener('click', e => {
    garantiaServicio();
});

// Evento para eliminar un detalle de garantía
document.getElementById('tbl_garantia').addEventListener('click', e => {
    let detalle_garantia_id = parseInt(e.target.getAttribute('detalle_garantia_id'));
    let garantia_id = parseInt(e.target.getAttribute('garantia_id'));
    if (detalle_garantia_id){
        eliminarGarantia({detalle_garantia_id: detalle_garantia_id});
        setTimeout(() => verGarantia(garantia_id), 500);
    }
});

// El costo del servicio se maneja en la vista del técnico, no aquí
