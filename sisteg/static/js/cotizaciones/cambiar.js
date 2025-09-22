//import { listarCarrito } from "./listarCarrito.js";
import { selectCliente } from "./selectCliente.js";
import { selectTipoPago } from "./selectTipoPago.js";
import { listar as listado } from './listar.js';
import { selectTipoServicio } from "./selectTipoServicio.js";
import { selectRolUsuario } from "./selectRolUsuario.js";

// Función para cambiar de vista entre el formulario y el listado de ventas
export function cambiar(selectedClienteId = null) {

    // Obtener elementos del DOM con verificación robusta
    const btn_agregar = document.getElementById('agregar');
    const form_agregar = document.getElementById('form_agregar');
    const listar = document.getElementById('listar');
    const crear_cotizacion = document.getElementById('crear_cotizacion');
    const eliminar_cotizacion = document.getElementById('eliminar_cotizacion');
    const actualizar_cotizacion = document.getElementById('actualizar_cotizacion');
    const finalizar_cotizacion = document.getElementById('finalizar_cotizacion');
    document.getElementById('telefono').innerHTML = '';
    document.getElementById('tbl_listar_carrito').childNodes[3].innerHTML = '';
    document.getElementById('subtotal').innerHTML = 'Q 0.0';

    // Verificar elementos críticos
    if (!btn_agregar) {
        console.error('Elemento "agregar" no encontrado');
        return;
    }
    if (!form_agregar) {
        console.error('Elemento "form_agregar" no encontrado');
        return;
    }
    if (!listar) {
        console.error('Elemento "listar" no encontrado');
        return;
    }

    // Resetear formulario
    try {
        form_agregar.reset();
    } catch (error) {
        console.error('Error al resetear formulario:', error);
    }

    // Limpiar atributo servicio_id si existe
    if (actualizar_cotizacion) {
        actualizar_cotizacion.removeAttribute('servicio_id');
        actualizar_cotizacion.hidden = true;
    }

    // Configurar botones con verificación
    if (crear_cotizacion) {
        crear_cotizacion.hidden = false;
    }
    if (eliminar_cotizacion) {
        eliminar_cotizacion.hidden = true;
    }
    if (finalizar_cotizacion) {
        finalizar_cotizacion.hidden = true;
    }

    // Alternar entre listado y formulario
    const estaOcultoListado = listar.style.display === 'none' || listar.hidden;

    if (estaOcultoListado) {
        // Mostrar listado, ocultar formulario
        btn_agregar.innerHTML = '<i class="fa-solid fa-square-plus"></i>';
        listar.style.display = 'block';
        listar.hidden = false;
        form_agregar.style.display = 'none';
        form_agregar.hidden = true;
        listado();
    } else {
        // Mostrar formulario, ocultar listado
        btn_agregar.innerHTML = '<i class="fa-solid fa-list"></i>';
        listar.style.display = 'none';
        listar.hidden = true;
        form_agregar.style.display = 'block';
        form_agregar.hidden = false;
        //listarCarrito();

        // Cargar datos para el formulario
        setTimeout(() => {
            selectTipoPago();
            selectTipoServicio();
            selectRolUsuario();

            // Solo cargar selectCliente si no hay datos en el carrito (modo creación)
            const carrito = document.getElementById('tbl_listar_carrito');
            const tieneDatos = carrito && carrito.querySelector('tbody tr');

            if (!tieneDatos) {
                selectCliente();
            }
        }, 100);
    }
}