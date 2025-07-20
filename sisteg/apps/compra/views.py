from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.db import transaction, IntegrityError, connection
from django.db.models import F
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import logging
logger = logging.getLogger(__name__)

from .models import Proveedor, Compra, DetalleCompra
from apps.producto.models import Producto
from apps.inicio.models import TipoPago

@login_required(login_url='autenticacion')
def vista_compra(request):
    return render(request, 'compra/compra.html')

@login_required(login_url='autenticacion')
def vista_proveedor(request):
    return render(request, 'proveedor/proveedor.html')

# Función para agregar proveedor
@login_required(login_url='autenticacion')
def agregar_proveedor(request):
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
        empresa = request.POST.get('empresa', '').strip().upper() or ''
        # Creamos el proveedor
        try:
            proveedor = Proveedor.objects.update_or_create(
                id = id,
                defaults = {
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'nit': nit,
                    'cui': cui,
                    'telefono': telefono,
                    'direccion': direccion,
                    'correo': correo,
                    'empresa': empresa,
                    'usuario_id': User.objects.get(id = request.user.id)
                }
            )
            res = True
            # Evaluamos si fue un nuevo registro o una actualización
            if proveedor[1]:
                msg = 'Proveedor agregada correctamente.'
            else:
                msg = 'Proveedor actualizada correctamente.'
        except:
            res = False
            msg = 'Hubo un error al agregar proveedor, actualice la página y vuleve a intentarlo.'
        # Retornamos una respuesta de éxito
        return JsonResponse({'res': res, 'msg': msg})
    else: # En caso contrario
        # Retornamos una respuesta de error
        return JsonResponse({'res': res, 'msg': msg})
    
# Función para listar proveedores
@login_required(login_url='autenticacion')
def listar_proveedor(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar proveedores.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    proveedores = ''

    try:
        if id: # Verificamos si necesitamos un proveedor en expecífico
            proveedores = Proveedor.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            proveedores = Proveedor.objects.filter(
                Q(nombres__icontains = buscar) |# Si hay buscamos por nombres
                Q(apellidos__icontains = buscar) |# Si hay buscamos por apellidos
                Q(nit__icontains = buscar) |# Si hay buscamos por nit
                Q(cui__icontains = buscar) # Si hay buscamos por cui
            )
        else:
            # Obtenemos todas los proveedores
            proveedores = Proveedor.objects.all()
            
        # Paginamos los proveedores
        paginador = Paginator(proveedores, 10)
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
                    'empresa': prov.empresa,
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
        msg = 'Listado de proveedores.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

# Función para crear compra
@login_required(login_url='autenticacion')
def agregar_compra(request):
    res = False
    msg = 'Método no permitido'
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id', '').strip()
        tipo_pago_id = request.POST.get('tipo_pago_id', '').strip()
        producto_id = request.POST.get('producto_id', '').strip()
        cantidad = request.POST.get('cantidad', '1')

        # Validación para proveedor_id
        if not proveedor_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione el proveedor.'})

        try:
            proveedor_id = int(proveedor_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione un proveedor válido.'})

        # Validación para tipo_pago_id
        if not tipo_pago_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione el tipo de pago.'})

        try:
            tipo_pago_id = int(tipo_pago_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione un tipo de pago válido.'})
        
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
        except:
            producto = None

        if producto: # Comprobamos si hay producto
            # Verificamos si existe una compra activa del usuario logeado
            existe_compra = Compra.objects.filter(usuario_id = request.user.id, estado = False)
            if existe_compra.exists(): # Si es así
                # Verificar si existe el producto en carrito
                existe_detalle = DetalleCompra.objects.filter(compra_id = existe_compra[0].id, producto_id = producto.id)
                if existe_detalle.exists(): # Si existe
                    # Creamos los nuevos valores del detalle de compra
                    cantidad_nueva = int(existe_detalle[0].cantidad) + int(cantidad)
                    total = float(existe_detalle[0].costo) * cantidad_nueva
                    # Actualizamos detalle de compra
                    existe_detalle.update(
                        cantidad = cantidad_nueva,
                        total = total
                    )
                else: # En caso contrario agregar el producto al carrito (compra)
                    detalle = DetalleCompra.objects.create(
                        costo = producto.costo,
                        cantidad = cantidad,
                        total = producto.costo,
                        producto_id = producto,
                        compra_id = existe_compra[0]
                    )
                    # Gaurdamos registro
                    detalle.save()
                # Creamos los nuevos valores para la compra
                todos_detalle = DetalleCompra.objects.filter(compra_id = existe_compra[0].id)
                subtotal = sum(dc.total for dc in todos_detalle)
                # Actualizamos la compra
                existe_compra.update(
                    subtotal = subtotal,
                    proveedor_id = proveedor_id,
                    tipo_pago_id = tipo_pago_id
                )
                # Datos de respuesta
                res = True
                msg = 'Carrito actualizado.'
            else: # En caso contrario
                compra = Compra.objects.create( # Creamos la compra
                    subtotal = producto.costo,
                    proveedor_id = Proveedor.objects.get(id = proveedor_id),
                    usuario_id = User.objects.get(id = request.user.id),
                    tipo_pago_id = TipoPago.objects.get(id = tipo_pago_id)
                )
                # Con su detalle
                detalle_compra = DetalleCompra.objects.create(
                    costo = producto.costo,
                    cantidad = cantidad,
                    total = producto.costo,
                    producto_id = producto,
                    compra_id = compra
                )
                # Gaurdamos los resgitros
                compra.save()
                detalle_compra.save()
                # Prepamos respuesta
                res = True
                msg = 'Compra agregada.'
        else:
            print(producto)

    return JsonResponse({'res': res, 'msg': msg})

# Función para eliminar compra
@login_required(login_url='autenticacion')
def eliminar_compra(request):
    # Varialbles por defectos
    res = False
    msg = 'Método no permitido.'
    if request.method == 'POST':
        # Capturamos los datos por POST
        detalle_compra_id = request.POST.get('detalle_compra_id', '').strip()
        compra_id = request.POST.get('compra_id', '').strip()
        # Sanitizamos los datos capturados
        if not detalle_compra_id:
            detalle_compra_id = None
        try:
            detalle_compra_id = int(detalle_compra_id)
        except (ValueError, TypeError):
            detalle_compra_id = None

        if not compra_id:
            compra_id = None
        try:
            compra_id = int(compra_id)
        except (ValueError, TypeError):
            compra_id = None

        # Procedemos a eliminar la compra
        try:
            # Primero comprobamos si hay id válido
            if detalle_compra_id is not None:
                # Obtenemos el registro del detalle de compra
                detalle_compra = DetalleCompra.objects.get(id = detalle_compra_id)
                # Obtenemos el registro de la compra como tal
                compra = Compra.objects.get(id = detalle_compra.compra_id.id)
                # Otenemos el total de registros en la compra
                detalle_compra_total = DetalleCompra.objects.filter(compra_id = compra.id).count()
                # Si solo tiene un detalle la compra
                if detalle_compra_total == 1:
                    compra.delete() # Eliminamos la compra completa
                    # Mensja de respuesta
                    msg = 'Carrito vaciado.'
                else:
                    # Solo eliminamos el detalle de la compra
                    detalle_compra.delete()
                    # Actualizamos la compra
                    subtotal = sum(dt.total for dt in DetalleCompra.objects.filter(compra_id = compra.id))
                    compra.subtotal = subtotal
                    compra.save()
                    # Mensaje de respuesta
                    msg = 'Carrito actualizado.'
                # Preparamos variables de respuesta
            elif compra_id is not None:
                # Obtenemos la compra
                compra = Compra.objects.get(id = compra_id)
                # Eliminamos la compra
                compra.delete()
                msg = 'Carrito vaciado.'
            res = True
        except:
            res = False
            msg = 'Hubo un error al eliminar el registro, actualice la página y vuelve a intentarlo.'
    return JsonResponse({'res': res, 'msg': msg})

# Función para listar carrito
@login_required(login_url='autenticacion')
def listar_carrito(request):
        # Mensajes de respuesta
    res = False
    msg = 'Error al listar carrito.'
    data = {}
    data['data'] = []
    try:
        compra = Compra.objects.get(usuario_id = request.user, estado = False)
        if compra:
            carrito = DetalleCompra.objects.filter(compra_id = compra)

            for carr in carrito:
                data['data'].append(
                    {
                        'id': carr.id,
                        'costo': carr.costo,
                        'cantidad': carr.cantidad,
                        'total': carr.total,
                        'producto': carr.producto_id.descripcion
                    }
                )
            data['carrito_id'] = compra.id
            data['subtotal'] = compra.subtotal
            data['tipo_pago_id'] = compra.tipo_pago_id.id
            data['proveedor_id'] = compra.proveedor_id.id
            # Preparamos mensajes de respuesta
            res = True
            msg = 'Elementos del carrito.'
        else:
            msg = 'El carrito está vació.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

@login_required(login_url='autenticacion')
def confirmar_compora(request):
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
        proveedor_id = data['proveedor_id']
        tipo_pago_id = data['tipo_pago_id']
        compra_id = data['compra_id']

        with transaction.atomic():
            # Registrar estado al entrar en bloque atómico
            logger.info("--- DENTRO DE BLOQUE ATOMIC ---")
            log_transaction_status()
            
            # Bloqueamos los registros
            compra = Compra.objects.select_for_update().get(id=compra_id)
            proveedor = Proveedor.objects.select_for_update().get(id=proveedor_id)
            tipo_pago = TipoPago.objects.select_for_update().get(id=tipo_pago_id)
            
            detalles = DetalleCompra.objects.filter(
                compra_id=compra.id
            ).select_related('producto_id').select_for_update()
            
            # Actualización de stock con seguimiento
            for dc in detalles:
                producto = dc.producto_id
                old_stock = producto.stock
                new_stock = old_stock + dc.cantidad
                
                # Actualización directa
                Producto.objects.filter(id=producto.id).update(stock=new_stock)
                
                logger.info(f"Stock actualizado: Producto {producto.id} "
                            f"de {old_stock} a {new_stock}")
            
            # Asignación correcta
            compra.estado = True
            compra.proveedor_id = proveedor
            compra.tipo_pago_id = tipo_pago
            compra.save()
            
            logger.info("Compra confirmada exitosamente")
            return JsonResponse({'res': True, 'msg': 'Compra realizada satisfactoriamente.'})
            
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

# Función para listar compras
@login_required(login_url='autenticacion')
def listar_compras(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar compras.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    compras = ''

    try:
        if id: # Verificamos si necesitamos una compra en expecífico
            compras = Compra.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            compras = Compra.objects.filter(
                Q(usuario_id__username__icontains = buscar) |# Si hay buscamos por usuario
                Q(proveedor_id__nombres__icontains = buscar) |# Si hay buscamos por nombre del proveedor
                Q(proveedor_id__apellidos__icontains = buscar) # Si hay buscamos por apellidos del proveedor
            )
        else:
            # Obtenemos todas las compras
            compras = Compra.objects.all()
            
        # Paginamos las compras
        paginador = Paginator(compras, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for com in paginas:
            data['data'].append(
                {
                    'id': com.id,
                    'subtotal': com.subtotal,
                    'fecha_ingreso': com.fecha_ingreso,
                    'fecha_actualizacion': com.fecha_actualizcion,
                    'tipo_pago': com.tipo_pago_id.descripcion,
                    'usuario_id': com.usuario_id.username,
                    'proveedor': f'{com.proveedor_id.nombres} {com.proveedor_id.apellidos}'
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
        msg = 'Listado de compras.'
    except Exception as e:
        print(f'\nSe generó un error a listar las compras.')
        print(f'El error es: {e}\n')
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)