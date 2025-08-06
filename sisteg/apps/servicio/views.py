from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.db import transaction, connection

from .models import Cliente, Servicio, DetalleServicio, TipoServicio
from apps.producto.models import Producto
from apps.inicio.models import TipoPago

import logging
logger = logging.getLogger(__name__)

@login_required(login_url='autenticacion')
def vista_cliente(request):
    return render(request, 'cliente/cliente.html')

@login_required(login_url='autenticacion')
def vista_servicio(request):
    return render(request, 'servicio/servicio.html')

@login_required(login_url='autenticacion')
def vista_venta(request):
    return render(request, 'venta/venta.html')

# Función para agregar cliente
@login_required(login_url='autenticacion')
def agregar_cliente(request):
    # Mensaje de respuesta
    res = False
    msg = '¡Método no permitido!'
    # Evaluamos si es llamado por POST
    if request.method == 'POST':
        # Capturamos los métodos por POST
        id = request.POST.get('id', None) or None
        nombres = request.POST.get('nombres', '').strip().upper() or ''
        apellidos = request.POST.get('apellidos', '').strip().upper() or ''
        nit = request.POST.get('nit', '').strip().upper() or ''
        cui = request.POST.get('cui', '').strip().upper() or ''
        telefono = request.POST.get('telefono', '').strip().upper() or ''
        direccion = request.POST.get('direccion', '').strip().upper() or ''
        correo = request.POST.get('correo', '').strip().upper() or ''
        # Creamos el cliente
        try:
            proveedor = Cliente.objects.update_or_create(
                id = id,
                defaults = {
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'nit': nit,
                    'cui': cui,
                    'telefono': telefono,
                    'direccion': direccion,
                    'correo': correo,
                    'usuario_id': User.objects.get(id = request.user.id)
                }
            )
            res = True
            # Evaluamos si fue un nuevo registro o una actualización
            if proveedor[1]:
                msg = 'Cliente agregada correctamente.'
            else:
                msg = 'Cliente actualizada correctamente.'
        except:
            res = False
            msg = 'Hubo un error al agregar cliente, actualice la página y vuleve a intentarlo.'
        # Retornamos una respuesta de éxito
        return JsonResponse({'res': res, 'msg': msg})
    else: # En caso contrario
        # Retornamos una respuesta de error
        return JsonResponse({'res': res, 'msg': msg})
    
# Función para listar clientes
@login_required(login_url='autenticacion')
def listar_cliente(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar clientes.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    clientes = ''

    try:
        if id: # Verificamos si necesitamos un cliente en expecífico
            clientes = Cliente.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            clientes = Cliente.objects.filter(
                Q(nombres__icontains = buscar) |# Si hay buscamos por nombres
                Q(apellidos__icontains = buscar) |# Si hay buscamos por apellidos
                Q(nit__icontains = buscar) |# Si hay buscamos por nit
                Q(cui__icontains = buscar) # Si hay buscamos por cui
            )
        else:
            # Obtenemos todas los clientes
            clientes = Cliente.objects.all()
            
        # Paginamos los clientes
        paginador = Paginator(clientes, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for prov in paginas:
            data['data'].append(
                {
                    'id': prov.id,
                    'nombres': prov.nombres,
                    'apellidos': prov.apellidos,
                    'nit': prov.nit,
                    'cui': prov.cui,
                    'telefono': prov.telefono,
                    'direccion': prov.direccion,
                    'correo': prov.correo,
                    'fecha_ingreso': prov.fecha_ingreso,
                    'fecha_actualizacion': prov.fecha_actualizacion,
                    'usuario': prov.usuario_id.username
                }
            )
        # Preparamos la visualización de las páginas
        if paginador.num_pages > 5:
            start = int(pagina)
            end = int(pagina) + 5
            if end > paginador.num_pages:
                start = paginador.num_pages - 4
                end = paginador.num_pages + 1
            for i in range(start, end):
                data["page_range"].append(i)
        else:
            for i in range(paginador.num_pages):
                data["page_range"].append(i + 1)
        data["num_pages"] = paginador.num_pages
        data["has_next"] = paginas.has_next()
        data["has_previous"] = paginas.has_previous()
        data["count"] = paginador.count

        # Preparamos mensajes de respuesta
        res = True
        msg = 'Listado de clientes.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

# Función para crear venta
@login_required(login_url='autenticacion')
def agregar_servicio(request):
    res = False
    msg = 'Método no permitido'
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id', '').strip()
        cliente_id = request.POST.get('cliente_id', '').strip()
        tipo_pago_id = request.POST.get('tipo_pago_id', '').strip()
        producto_id = request.POST.get('producto_id', '').strip()
        tipo_servicio_id = request.POST.get('tipo_servicio_id', '').strip()
        cantidad = request.POST.get('cantidad', '1')
        stock = request.POST.get('stock', '').strip()

        # Validación para cliente_id
        if not servicio_id:
            servicio_id = None

        try:
            servicio_id = int(servicio_id)
        except (ValueError, TypeError):
            servicio_id = None
        
        # Validación para cliente_id
        if not cliente_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione el cliente.'})

        try:
            cliente_id = int(cliente_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione un cliente válido.'})

        # Validación para tipo_pago_id
        if not tipo_pago_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione el tipo de pago.'})

        try:
            tipo_pago_id = int(tipo_pago_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione un tipo de pago válido.'})
        
        # Validación para tipo_servicio_id
        if not tipo_servicio_id:
            tipo_servicio_id = 1

        try:
            tipo_pago_id = int(tipo_pago_id)
        except (ValueError, TypeError):
            tipo_servicio_id = 1
        
        # Validación para stock si es true o false
        if not stock:
            stock = True

        try:
            stock = int(stock)
            if stock == 1:
                stock = True
            else:
                stock = False
        except (ValueError, TypeError):
            stock = True
        
        # Validación para producto_id
        if not producto_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione un producto'})
        
        # Validación de la cantidad que siempre sea un entero positivo
        if cantidad.strip() == '': # Si la cantidad es una cadena vacía le asignamos valor 1
            cantidad = 1
        try: # Convertimos un cantidad en entero
            cantidad = int(cantidad)
        except ValueError: # En caso de error le asignamos 1
            cantidad = 1
        if cantidad <= 0: # Caso de que cantidad sea 0 o menor que cero, le asignamos 1
            cantidad = 1

        try:
            producto_id = int(producto_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione un producto válido.'})

        try:
            producto = Producto.objects.get(id = producto_id)
            if cantidad > producto.stock:
                return JsonResponse({'res': False, 'msg': f'El stock del producto es insuficiente, solo hay {producto.stock} en existencia.'})
        except:
            producto = None

        if producto: # Comprobamos si hay producto
            # Verificamos si existe una venta activa del usuario logeado
            if servicio_id:
                existe_servicio = Servicio.objects.filter(id = servicio_id)
            else:
                existe_servicio = Servicio.objects.filter(usuario_id = request.user.id, estado = False, tipo_servicio_id = 1)
            print('\n------------------------------------------------')
            print(existe_servicio)
            print(f'servicio_id: {servicio_id}')
            print('------------------------------------------------\n')
            if existe_servicio.exists(): # Si es así
                # Verificar si existe el producto en carrito
                existe_detalle = DetalleServicio.objects.filter(servicio_id = existe_servicio[0].id, producto_id = producto.id)
                if existe_detalle.exists(): # Si existe
                    # Creamos los nuevos valores del detalle de venta
                    if cantidad == 1:
                        cantidad_nueva = int(cantidad)
                    else:
                        cantidad_nueva = cantidad
                    total = float(existe_detalle[0].precio) * cantidad_nueva
                    # Actualizamos detalle de venta
                    existe_detalle.update(
                        cantidad = cantidad_nueva,
                        total = total,
                        ganancia = producto.precio - producto.costo,
                        stock = stock
                    )
                else: # En caso contrario agregar el producto al carrito (venta)
                    detalle = DetalleServicio.objects.create(
                        precio = producto.precio,
                        costo = producto.costo,
                        cantidad = cantidad,
                        total = producto.precio,
                        ganancia = producto.precio - producto.costo,
                        stock = stock,
                        producto_id = producto,
                        servicio_id = existe_servicio[0]
                    )
                    # Gaurdamos registro
                    detalle.save()
                # Creamos los nuevos valores para la venta
                todos_detalle = DetalleServicio.objects.filter(servicio_id = existe_servicio[0].id)
                subtotal = sum(dc.total for dc in todos_detalle)
                # Actualizamos la venta
                existe_servicio.update(
                    subtotal = subtotal,
                    cliente_id = cliente_id,
                    tipo_pago_id = tipo_pago_id
                )
                # Datos de respuesta
                res = True
                msg = 'Carrito actualizado.'
            else: # En caso contrario
                servicio = Servicio.objects.create( # Creamos la servicio
                    subtotal = producto.precio,
                    cliente_id = Cliente.objects.get(id = cliente_id),
                    usuario_id = User.objects.get(id = request.user.id),
                    tipo_pago_id = TipoPago.objects.get(id = tipo_pago_id),
                    tipo_servicio_id = TipoServicio.objects.get(id = tipo_servicio_id)
                )
                # Con su detalle
                detalle_servicio = DetalleServicio.objects.create(
                    precio = producto.precio,
                    costo = producto.costo,
                    cantidad = cantidad,
                    total = producto.precio,
                    ganancia = producto.precio - producto.costo,
                    stock = stock,
                    producto_id = producto,
                    servicio_id = servicio
                )
                # Gaurdamos los resgitros
                servicio.save()
                detalle_servicio.save()
                # Prepamos respuesta
                res = True
                msg = 'Servicio agregada.'
        else:
            print(producto)
    return JsonResponse({'res': res, 'msg': msg})

# Función para listar carrito
@login_required(login_url='autenticacion')
def listar_carrito(request):
    # Capturar id de servicio
    servicio_id = request.GET.get('servicio_id', None) or None
    print('\n------------------------------------')
    print(f'servicio id: {servicio_id}')
    print('------------------------------------\n')
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar carrito.'
    data = {}
    data['data'] = []
    try:
        if servicio_id:
            servicio = Servicio.objects.filter(id = servicio_id)
        else:
            # Evaluamos si es una venta el servicio
            servicio = Servicio.objects.filter(usuario_id = request.user, estado = False, tipo_servicio_id = 1)

        if servicio:
            carrito = DetalleServicio.objects.filter(servicio_id = servicio[0].id)
            for carr in carrito:
                data['data'].append(
                    {
                        'id': carr.id,
                        'precio': carr.precio,
                        'cantidad': carr.cantidad,
                        'total': carr.total,
                        'producto': carr.producto_id.descripcion,
                        'marca': carr.producto_id.marca_id.descripcion,
                        'producto_id': carr.producto_id.id
                    }
                )
            data['carrito_id'] = servicio[0].id
            data['subtotal'] = servicio[0].subtotal
            data['tipo_pago_id'] = servicio[0].tipo_pago_id.id
            data['proveedor_id'] = servicio[0].cliente_id.id
            # Preparamos mensajes de respuesta
            res = True
            msg = 'Elementos del carrito.'
        else:
            msg = 'El carrito está vació.'
    except Exception as e:
        print(e)
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

# Funcionalidad de confirmar servicio
@login_required(login_url='autenticacion')
def confirmar_servicio(request):
    def log_transaction_status():
        """Función para registrar el estado de la transacción"""
        try:
            logger.info(f"Autocommit: {connection.get_autocommit()}")
            logger.info(f"En transacción: {connection.in_atomic_block}")
            # Solo intentar obtener nivel de aislamiento para PostgreSQL
            if connection.vendor == 'postgresql' and hasattr(connection, 'get_isolation_level'):
                logger.info(f"Nivel de aislamiento: {connection.get_isolation_level()}")
        except Exception as e:
            logger.error(f"Error al verificar estado de transacción: {str(e)}")

    try:
        # Verificación inicial de transacción
        logger.info("=== INICIO DE SOLICITUD ===")
        log_transaction_status()

        if request.method != 'POST':
            return JsonResponse({'res': False, 'msg': 'Método no permitido.'})
        
        # Parseo fuera del bloque atómico
        data = json.loads(request.body)
        cliente_id = data['cliente_id']
        tipo_pago_id = data['tipo_pago_id']
        servicio_id = data['servicio_id']

        with transaction.atomic():
            # Registrar estado al entrar en bloque atómico
            logger.info("--- DENTRO DE BLOQUE ATOMIC ---")
            log_transaction_status()
            
            # Bloqueamos los registros
            servicio = Servicio.objects.select_for_update().get(id=servicio_id)
            cliente = Cliente.objects.select_for_update().get(id=cliente_id)
            tipo_pago = TipoPago.objects.select_for_update().get(id=tipo_pago_id)
            
            detalles = DetalleServicio.objects.filter(
                servicio_id=servicio.id
            ).select_related('producto_id').select_for_update()
            
            # Antes de descontar el stock verificar si hay stock suficiente
            for dc in detalles:
                producto = dc.producto_id
                if producto.stock < dc.cantidad:
                    return JsonResponse({'res': False, 'msg': f'El producto {producto.descripcion} tiene stock insuficiente, solo hay {producto.stock} en existencia.'})

            # Actualización de stock con seguimiento
            for dc in detalles:
                if dc.stock:
                    producto = dc.producto_id
                    old_stock = producto.stock
                    new_stock = old_stock - dc.cantidad
                
                # Actualización directa
                Producto.objects.filter(id=producto.id).update(stock=new_stock)
                
                logger.info(f"Stock actualizado: Producto {producto.id} "
                            f"de {old_stock} a {new_stock}")
            
            # Asignación correcta
            servicio.estado = True
            servicio.cliente_id = cliente
            servicio.tipo_pago_id = tipo_pago
            servicio.save()
            
            logger.info("Servicio confirmada exitosamente")
            return JsonResponse({'res': True, 'msg': 'Servicio realizada satisfactoriamente.'})
            
    except Exception as e:
        logger.error(f"ERROR: {str(e)}", exc_info=True)
        
        # Verificación detallada del estado de transacción
        logger.error("=== ESTADO DE TRANSACCIÓN AL PRODUCIRSE ERROR ===")
        log_transaction_status()
        
        # Intento de rollback manual
        try:
            if connection.in_atomic_block:
                transaction.set_rollback(True)
                logger.warning("Rollback manual ejecutado")
        except Exception as rollback_error:
            logger.critical(f"Fallo en rollback manual: {str(rollback_error)}")
        
        return JsonResponse({
            'res': False, 
            'msg': f'Error: {str(e)}. Transacción revertida.'
        }, status=500)