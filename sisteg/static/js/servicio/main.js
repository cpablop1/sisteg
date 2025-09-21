import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { validacion } from './validacion.js';
import { listarProductos } from './listarProductos.js';
import { eliminarServicio } from './eliminarServicio.js';
import { finalizarServicio } from './finalizarServicio.js';
import { listarDetalleServicio } from './listarDetalleServicio.js';
import { editarServicio } from './EditarServicio.js';
import { ticketPdf } from './ticketPdf.js';
import { verGarantia } from './verGarantia.js';
import { garantiaServicio } from './garantiaServicio.js';
import { eliminarGarantia } from './eliminarGarantia.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-gear"></i> Servicio`;
    document.getElementById('agregar').innerHTML = '';
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

// Evento para mostrar modal de buscar productos
document.getElementById('btn-buscar-productos').addEventListener('click', e => {
    new bootstrap.Modal(document.getElementById('mdl_buscar_productos')).show();
    setTimeout(() => listarProductos(), 500);
});

// Evento para agregar productos al servicio
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

// Evento para buscar servicios
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({ 'tipo_servicio': 'venta', 'pagina': 1, 'buscar': buscar });
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

// Evento para actualizar cantidad, costo y precio en carrito de servicio
document.getElementById('tbl_listar_carrito').addEventListener('click', e => {
    let producto_id = parseInt(e.target.getAttribute('producto_id'));
    if (producto_id) {
        let form = document.getElementById('form_agregar');
        let cantidad = parseInt(document.getElementById(`cantidad${producto_id}`).value);
        let costo = parseFloat(document.getElementById(`costo${producto_id}`).value);
        let precio = parseFloat(document.getElementById(`precio${producto_id}`).value);
        let stock = document.getElementById(`stock${producto_id}`).checked ? 1 : 0;

        if (validacion(form)) {
            if (cantidad && (costo < precio)) {
                agregar(form, producto_id, cantidad, costo, precio, stock)
            } else {
                alerta.danger('Verifique la cantidad que se válida o el costo se que se menor a precio.');
            }
        } else {
            alerta.warning('Complete el formulario para continuar.');
        }
    } else {
        console.log('Evento nada que ver...');
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

// Evento para mostrar servicio a editar
document.getElementById('tbl_listar').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('editar_servicio_id'));
    if (servicio_id) {
        cambiar();
        editarServicio(servicio_id);
    }
});

// Evento para editar servicio
document.getElementById('actualizar_servicio').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    let form = document.getElementById('form_agregar');
    if (servicio_id) {
        agregar(form);
        //cambiar();
        setTimeout(() => {
            editarServicio(servicio_id);
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

// Evento para mostra modal de garantía
document.getElementById('garantia_servicio').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'))
    let garantia_id = parseInt(e.target.getAttribute('garantia_id'))
    document.getElementById('form_garantia').reset();
    let crear_garantia = document.getElementById('crear_garantia');
    if (servicio_id) {
        new bootstrap.Modal(document.getElementById('mdl_garantia')).show();
        if (garantia_id) {
            setTimeout(() => verGarantia(garantia_id), 500);
        } else {
            document.getElementById('servicio_id').value = servicio_id;
            document.getElementById('tbl_garantia').childNodes[3].innerHTML = '';
            crear_garantia.innerHTML = '<i class="fa-solid fa-square-plus"></i> Crear';
            crear_garantia.classList.remove('btn-warning');
            crear_garantia.classList.add('btn-primary');
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
    console.log(garantia_id);
    if (detalle_garantia_id) {
        eliminarGarantia({ detalle_garantia_id: detalle_garantia_id });
        setTimeout(() => verGarantia(garantia_id), 500);
    }
});

// Evento para finalizar la servicio
document.getElementById('finalizar_servicio').addEventListener('click', e => {
    let servicio_id = parseInt(e.target.getAttribute('servicio_id'));
    let cliente_id = parseInt(document.getElementById('cliente_id').value);
    let tipo_pago_id = parseInt(document.getElementById('tipo_pago_id').value);
    console.log('Finaliando servicio');
    console.log(servicio_id);
    if (servicio_id) {
        finalizarServicio({ servicio_id: servicio_id, cliente_id: cliente_id, tipo_pago_id: tipo_pago_id });
    }
})