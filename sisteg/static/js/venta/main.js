import * as alerta from '../alertas/alertas.js';
import { cambiar } from './cambiar.js';
import { agregar } from './agregar.js';
import { listar } from './listar.js';
import { validacion } from './validacion.js';
import { listarProductos } from './listarProductos.js';
import { eliminarCompra } from './eliminarCompra.js';
import { confirmarCompra } from './confirmarCompra.js';
import { listarDetalleCompra } from './listarDetalleCompra.js';

window.onload = () => {
    let titulo = document.getElementById('titulo');
    titulo.innerHTML = `<i class="fa-solid fa-cart-shopping"></i> Venta`;
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

// Evento para cambiar de vista entre el carrito y el listado de compras
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

// Evento para buscar marcas
document.getElementById('buscar').addEventListener('input', e => {
    let buscar = e.target.value.trim();
    if (buscar.length > 0) {
        listar({ 'pagina': 1, 'buscar': buscar });
    } else {
        listar();
    }
});

// Evento para eliminar elementos de la compra
document.getElementById('tbl_listar_carrito').addEventListener('click', e => {
    let detalle_compra_id = parseInt(e.target.getAttribute('detalle_compra_id'));
    if (detalle_compra_id){
        eliminarCompra({'detalle_compra_id': detalle_compra_id});
    }
});

// Evento para eliminar la compra completa
document.getElementById('eliminar_compra').addEventListener('click', e => {
    let compra_id = parseInt(e.target.getAttribute('compra_id'));
    if (compra_id){
        eliminarCompra({'compra_id': compra_id});
    }
});

// Evento para confirmar la compra
document.getElementById('confirmar_compra').addEventListener('click', e => {
    let compra_id = parseInt(e.target.getAttribute('compra_id'));
    let proveedor_id = parseInt(document.getElementById('proveedor_id').value);
    let tipo_pago_id = parseInt(document.getElementById('tipo_pago_id').value);
    
    if (compra_id){
        confirmarCompra({compra_id: compra_id, proveedor_id: proveedor_id, tipo_pago_id: tipo_pago_id});
    }

})

// Evento para actualizar cantidad en carrito de compra
document.getElementById('tbl_listar_carrito').addEventListener('keyup', e => {
    let form = document.getElementById('form_agregar');
    let cantidad = parseInt(e.target.value);
    let producto_id = parseInt(e.target.getAttribute('producto_id'));
    if (validacion(form)) {
        if (e.keyCode == 13){
            if (cantidad) {
                console.log(cantidad);
                agregar(form, producto_id, cantidad)
            } else {
                alerta.danger('Ingrese una cantidad válida.');
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

// Evento para ver detalle de compra
document.getElementById('tbl_listar').addEventListener('click', e => {
    let compra_id = parseInt(e.target.getAttribute('compra_id'));
    if (compra_id){
        new bootstrap.Modal(document.getElementById('mdl_detalle_compra')).show();
        listarDetalleCompra(compra_id);
    }
});