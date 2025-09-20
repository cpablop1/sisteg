from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.db import transaction, connection

from .models import Cliente, Servicio, DetalleServicio, TipoServicio, ServicioUsuario, Garantia, DetalleGarantia
from apps.producto.models import Producto
from apps.inicio.models import TipoPago

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
#from reportlab.pdfgen import canvas
from io import BytesIO

from reportlab.lib.pagesizes import mm, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table
#from reportlab.lib.units import inch
#from reportlab.lib import colors

@login_required(login_url='autenticacion')
def vista_cliente(request):
    return render(request, 'cliente/cliente.html')

@login_required(login_url='autenticacion')
def vista_servicio(request):
    return render(request, 'servicio/servicio.html')

@login_required(login_url='autenticacion')
def vista_venta(request):
    return render(request, 'venta/venta.html')

@login_required(login_url='autenticacion')
def vista_mantenimiento(request):
    return render(request, 'servicio/mantenimiento.html')

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

# Función para listar tipos de servicio
@login_required(login_url='autenticacion')
def listar_tipo_servicio(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar tipo servicios.'
    data = {}
    data['data'] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    tipo_sercicios = ''

    try:
        if id: # Verificamos si necesitamos un tipo servicio en expecífico
            tipo_sercicios = TipoServicio.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            tipo_sercicios = TipoServicio.objects.filter(
                Q(descripcion__icontains = buscar) # Si hay buscamos por descripción
            )
        else:
            # Obtenemos todas los tipos de servicios
            tipo_sercicios = TipoServicio.objects.all()
        # Preparamos listado de los tipos de servicios
        for ts in tipo_sercicios:
            data['data'].append(
                {
                    'id': ts.id,
                    'descripcion': ts.descripcion
                }
            )

        # Preparamos mensajes de respuesta
        res = True
        msg = 'Listado de tipos de servicios.'
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
        rol_usuario_id = request.POST.get('rol_usuario_id', '').strip()
        cantidad = request.POST.get('cantidad', '1')
        stock = request.POST.get('stock', '').strip()
        observacion = request.POST.get('observacion', '').strip()
        nota = request.POST.get('nota', '').strip()
        costo_servicio = request.POST.get('costo_servicio', '0').strip()
        precio = request.POST.get('precio', '0').strip()
        costo = request.POST.get('costo', '0').strip()

        # Validación para rol_usuario_id
        if not rol_usuario_id:
            rol_usuario_id = None

        try:
            rol_usuario_id = int(rol_usuario_id)
        except (ValueError, TypeError):
            rol_usuario_id = None
        
        # Validación para tipo_servicio_id
        if not tipo_servicio_id:
            return JsonResponse({'res': False, 'msg': 'Seleccione el tipo de servicio'})

        try:
            tipo_servicio_id = int(tipo_servicio_id)
        except (ValueError, TypeError):
            return JsonResponse({'res': False, 'msg': 'Seleccione el tipo de servicio'})

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
        
        # Validación de la cantidad que siempre sea un entero positivo
        if cantidad.strip() == '': # Si la cantidad es una cadena vacía le asignamos valor 1
            cantidad = 1
        try: # Convertimos un cantidad en entero
            cantidad = int(cantidad)
        except ValueError: # En caso de error le asignamos 1
            cantidad = 1
        if cantidad <= 0: # Caso de que cantidad sea 0 o menor que cero, le asignamos 1
            cantidad = 1
        # Validación de la costo del servicio que siempre sea una decimal o un entero positivo
        if costo_servicio.strip() == '': # Si la cantidad es una cadena vacía le asignamos valor 0
            costo_servicio = 0
        try: # Convertimos un costo_servicio en decimal
            costo_servicio = float(costo_servicio)
        except ValueError: # En caso de error le asignamos 0
            costo_servicio = 0
        if costo_servicio <= 0: # Caso de que cantidad sea 0 o menor que cero, le asignamos 1
            costo_servicio = 0
        
        # Validación de la precio del detalle del servicio que siempre sea una decimal o un entero positivo
        if precio.strip() == '': # Si la cantidad es una cadena vacía le asignamos valor 0
            precio = 0
        try: # Convertimos un precio_servicio en decimal
            precio = float(precio)
        except ValueError: # En caso de error le asignamos 0
            precio = 0
        if precio <= 0: # Caso de que cantidad sea 0 o menor que cero, le asignamos 1
            precio = 0
        
        # Validación de la costo del detalle del servicio que siempre sea una decimal o un entero positivo
        if costo.strip() == '': # Si la cantidad es una cadena vacía le asignamos valor 0
            costo = 0
        try: # Convertimos un precio_servicio en decimal
            costo = float(costo)
        except ValueError: # En caso de error le asignamos 0
            costo = 0
        if costo <= 0: # Caso de que cantidad sea 0 o menor que cero, le asignamos 1
            costo = 0

        # Validación para producto_id
        if not producto_id:
            #return JsonResponse({'res': False, 'msg': 'Seleccione un producto'})
            producto_id = None

        try:
            producto_id = int(producto_id)
        except (ValueError, TypeError):
            producto_id = None

        try:
            producto = Producto.objects.get(id = producto_id)
            if cantidad > producto.stock:
                return JsonResponse({'res': False, 'msg': f'El stock del producto es insuficiente, solo hay {producto.stock} en existencia.'})
            if costo > precio:
                return JsonResponse({'res': False, 'msg': 'El costo debe ser menor al precio del servicio.'})
        except:
            producto = None

        if producto: # Comprobamos si hay producto
            # Verificamos si existe una venta activa del usuario logeado
            if servicio_id:
                existe_servicio = Servicio.objects.filter(id = servicio_id)
            else:
                if (request.rol_usuario == 'recepcionista' and (tipo_servicio_id != 1)):
                    return JsonResponse({'res': False, 'msg': 'No puedes agregar productos a un servicio de tipo mantenimiento'})
                existe_servicio = Servicio.objects.filter(usuario_id = request.user.id, estado = False, tipo_servicio_id = tipo_servicio_id)

            if existe_servicio.exists(): # Si es así
                # Verificar si existe el producto en carrito
                existe_detalle = DetalleServicio.objects.filter(servicio_id = existe_servicio[0].id, producto_id = producto.id)
                if existe_detalle.exists(): # Si existe
                    # Creamos los nuevos valores del detalle de venta
                    if cantidad == 1:
                        cantidad_nueva = int(cantidad)
                    else:
                        cantidad_nueva = cantidad
                    
                    # Usar precio del producto de la base de datos si el precio enviado es 0
                    precio_final = precio if precio > 0 else producto.precio
                    costo_final = costo if costo > 0 else producto.costo
                    
                    total = precio_final * cantidad_nueva
                    ganancia_unitaria = precio_final - costo_final
                    ganancia_total = ganancia_unitaria * cantidad_nueva
                    
                    # Creamos los nevos valores del los costo y precio del servicio
                    # Actualizamos detalle de venta
                    existe_detalle.update(
                        cantidad = cantidad_nueva,
                        costo = costo_final,
                        precio = precio_final,
                        total = total,
                        ganancia = ganancia_total,
                        stock = stock
                    )
                else: # En caso contrario agregar el producto al carrito (venta)
                    total_nuevo = producto.precio * cantidad
                    ganancia_unitaria_nueva = producto.precio - producto.costo
                    ganancia_total_nueva = ganancia_unitaria_nueva * cantidad
                    
                    
                    detalle = DetalleServicio.objects.create(
                        precio = producto.precio,
                        costo = producto.costo,
                        cantidad = cantidad,
                        total = total_nuevo,
                        ganancia = ganancia_total_nueva,
                        stock = stock,
                        producto_id = producto,
                        servicio_id = existe_servicio[0]
                    )
                    # Gaurdamos registro
                    detalle.save()
                # Creamos los nuevos valores para la venta
                todos_detalle = DetalleServicio.objects.filter(servicio_id = existe_servicio[0].id)
                subtotal = sum(dc.total for dc in todos_detalle)
                subtotal += costo_servicio
                #subtotal += existe_servicio[0].costo_servicio
                # Actualizamos la venta
                existe_servicio.update(
                    subtotal = subtotal,
                    costo_servicio = costo_servicio,
                    cliente_id = cliente_id,
                    tipo_pago_id = tipo_pago_id,
                )
                # Datos de respuesta
                res = True
                msg = 'Carrito actualizado.'
            else: # En caso contrario
                total_servicio = producto.precio * cantidad
                ganancia_unitaria_servicio = producto.precio - producto.costo
                ganancia_total_servicio = ganancia_unitaria_servicio * cantidad
                
                
                servicio = Servicio.objects.create( # Creamos el servicio
                    subtotal = total_servicio,
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
                    total = total_servicio,
                    ganancia = ganancia_total_servicio,
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
            servicio_usuario_id = None
            if tipo_servicio_id == 1:
                return JsonResponse({'res': False, 'msg': 'Una venta debe tener al menos un producto.'})
            if not rol_usuario_id:
                return JsonResponse({'res': False, 'msg': 'El servicio debe ser asignado a un ténico.'})
            # Actualizar subtotal
            detalle_servicio = ''
            subtotal = 0
            try:
                detalle_servicio = DetalleServicio.objects.filter(servicio_id = servicio_id)
                subtotal = sum(ds.total for ds in detalle_servicio)
                subtotal += costo_servicio
            except:
                subtotal = costo_servicio
            datos = {
                'subtotal': subtotal,
                'observacion': observacion,
                'nota': nota,
                'costo_servicio': costo_servicio,
                'cliente_id': Cliente.objects.get(id = cliente_id),
                'tipo_pago_id': TipoPago.objects.get(id = tipo_pago_id),
                'tipo_servicio_id': TipoServicio.objects.get(id = tipo_servicio_id)
            }
            if not servicio_id:
                datos['usuario_id'] = User.objects.get(id = request.user.id)
            
            servicio = Servicio.objects.update_or_create( # Creamos el servicio
                id = servicio_id,
                defaults = datos
            )
            # Evaluamos si fue un nuevo registro o una actualización
            if servicio[1]:
                msg = 'Servicio agregada correctamente.'
            else:
                servicio_usuario_id = ServicioUsuario.objects.get(servicio_id = servicio[0].id).id
                msg = 'Servicio actualizada correctamente.'
            
            # Y creamos el registro a quién se le asignó el servicio
            ServicioUsuario.objects.update_or_create(
                id = servicio_usuario_id,
                defaults = {
                    'usuario_id': User.objects.get(id = rol_usuario_id),
                    'servicio_id': servicio[0]
                }
            )
            return JsonResponse({'res': True, 'msg': msg})
    return JsonResponse({'res': res, 'msg': msg})

# Función para listar carrito
@login_required(login_url='autenticacion')
def listar_carrito(request):
    # Capturar id de servicio
    servicio_id = request.GET.get('servicio_id', '').strip()
    # Validación para servicio_id
    if not servicio_id:
        servicio_id = None
    try:
        servicio_id = int(servicio_id)
    except (ValueError, TypeError):
        servicio_id = None
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
            ganancia = 0
            for carr in carrito:
                ganancia += carr.ganancia
                data['data'].append(
                    {
                        'id': carr.id,
                        'precio': carr.precio,
                        'costo': carr.costo,
                        'ganancia': carr.ganancia,
                        'cantidad': carr.cantidad,
                        'total': carr.total,
                        'producto': carr.producto_id.descripcion,
                        'stock': carr.stock,
                        'marca': carr.producto_id.marca_id.descripcion,
                        'producto_id': carr.producto_id.id
                    }
                )
            data['carrito_id'] = servicio[0].id
            data['subtotal'] = servicio[0].subtotal
            data['ganancia'] = ganancia + servicio[0].costo_servicio
            data['tipo_pago_id'] = servicio[0].tipo_pago_id.id
            data['cliente_id'] = servicio[0].cliente_id.id
            data['cliente'] = f'{servicio[0].cliente_id.nombres} {servicio[0].cliente_id.apellidos}'
            data['contacto'] = servicio[0].cliente_id.telefono
            data['tipo_servicio_id'] = servicio[0].tipo_servicio_id.id
            data['observacion'] = servicio[0].observacion
            data['nota'] = servicio[0].nota
            data['costo_servicio'] = servicio[0].costo_servicio
            #data['rol_usuario_id'] = ServicioUsuario.objects.filter(servicio_id = servicio[0].id)[0].usuario_id.id
            try:
                data['garantia_id'] = Garantia.objects.get(servicio_id = servicio[0].id).id
            except Exception as e:
                data['garantia_id'] = False
                
            # Preparamos mensajes de respuesta
            res = True
            msg = 'Elementos del carrito.'
        else:
            msg = 'El carrito está vació.'
    except Exception as e:
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
    
# Función para eliminar servicio
@login_required(login_url='autenticacion')
def eliminar_servicio(request):
    # Varialbles por defectos
    res = False
    msg = 'Método no permitido.'
    if request.method == 'POST':
        # Capturamos los datos por POST
        detalle_servicio_id = request.POST.get('detalle_servicio_id', '').strip()
        servicio_id = request.POST.get('servicio_id', '').strip()
        # Sanitizamos los datos capturados
        if not detalle_servicio_id:
            detalle_servicio_id = None
        try:
            detalle_servicio_id = int(detalle_servicio_id)
        except (ValueError, TypeError):
            detalle_servicio_id = None

        if not servicio_id:
            servicio_id = None
        try:
            servicio_id = int(servicio_id)
        except (ValueError, TypeError):
            servicio_id = None

        # Procedemos a eliminar el servicio
        try:
            # Primero comprobamos si hay id válido
            if detalle_servicio_id is not None:
                # Obtenemos el registro del detalle del servicio
                detalle_servicio = DetalleServicio.objects.get(id = detalle_servicio_id)
                # Obtenemos el registro del servicio como tal
                servicio = Servicio.objects.get(id = detalle_servicio.servicio_id.id)
                # Otenemos el total de registros del servicio
                detalle_servicio_total = DetalleServicio.objects.filter(servicio_id = servicio.id).count()
                # Si solo tiene un detalle el servicio
                if detalle_servicio_total == 1:
                    if request.rol_usuario == 'tecnico':
                        detalle_servicio.delete()
                        subtotal = servicio.costo_servicio
                        servicio.subtotal = subtotal
                        servicio.save()
                    else:
                        servicio.delete() # Eliminamos el servicio completo
                    # Mensja de respuesta
                    msg = 'Carrito vaciado.'
                else:
                    # Solo eliminamos el detalle del servicio
                    detalle_servicio.delete()
                    # Actualizamos el servicio
                    subtotal = sum(dt.total for dt in DetalleServicio.objects.filter(servicio_id = servicio.id))
                    subtotal += servicio.costo_servicio
                    servicio.subtotal = subtotal
                    servicio.save()
                    # Mensaje de respuesta
                    msg = 'Carrito actualizado.'
                # Preparamos variables de respuesta
            elif servicio_id is not None:
                # Obtenemos el servicio
                servicio = Servicio.objects.get(id = servicio_id)
                if servicio.tipo_servicio_id.id != 1: # Evaluamos primero si existe una referencia en servicioUsuario
                    # Para luego eliminarla
                    servicio_usuario = ServicioUsuario.objects.get(servicio_id = servicio_id)
                    servicio_usuario.delete()
                # Eliminamos el servicio
                servicio.delete()
                msg = 'Carrito vaciado.'
            res = True
        except Exception as ex:
            print('\n--------------------------------')
            print(ex)
            print('--------------------------------\n')
            res = False
            msg = 'Hubo un error al eliminar el registro, actualice la página y vuelve a intentarlo.'
    return JsonResponse({'res': res, 'msg': msg})

# Función para listar servicios
@login_required(login_url='autenticacion')
def listar_servicios(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar servicios.'
    data = {}
    data['data'] = []
    data['detalle_servicio'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    servicios = ''
    detalle_servicio = ''

    try:
        if id: # Verificamos si necesitamos un servicio en expecífico
            servicios = Servicio.objects.filter(id = id)
            detalle_servicio = DetalleServicio.objects.filter(servicio_id = id)
        else: # Sino se lista todos menos los de tipo ventas
            # Obtener tipo_servicio del parámetro GET
            tipo_servicio = request.GET.get('tipo_servicio', '').strip()
            
            if request.rol_usuario == 'tecnico': # Filtramos los registros is el usuario es ténico
                servicios = []
                # Obtener todos los servicios asociados al usuario técnico
                servicio_usuario = ServicioUsuario.objects.filter(usuario_id = request.user.id)
                # Extraer los IDs de los servicios en una lista
                servicio_ids = servicio_usuario.values_list('servicio_id', flat=True)
                # Filtrar todos los servicios cuyos IDs están en la lista
                servicios = Servicio.objects.filter(id__in=servicio_ids)
                # Filtrar por tipo de servicio si se especifica
                if tipo_servicio:
                    if tipo_servicio == 'venta':
                        servicios = servicios.filter(tipo_servicio_id=1)
                    elif tipo_servicio == 'mantenimiento':
                        servicios = servicios.exclude(tipo_servicio_id=1)  # Excluir solo ventas, mostrar todo lo demás
            else:
                servicios = Servicio.objects.all()
                
                # Filtrar por tipo de servicio si se especifica
                if tipo_servicio:
                    if tipo_servicio == 'venta':
                        servicios = servicios.filter(tipo_servicio_id=1)
                    elif tipo_servicio == 'mantenimiento':
                        servicios = servicios.exclude(tipo_servicio_id=1)  # Excluir solo ventas, mostrar todo lo demás
        if len(buscar) > 0: # Verificamos si hay búsquedad
            servicios = servicios.filter(
                Q(usuario_id__username__icontains = buscar) |# Si hay buscamos por usuario
                Q(cliente_id__nombres__icontains = buscar) |# Si hay buscamos por nombre del cliente
                Q(cliente_id__apellidos__icontains = buscar) |# Si hay buscamos por apellidos del cliente
                Q(tipo_servicio_id__descripcion__icontains = buscar) # Si hay buscamos por tipo servicio
            )
            
        # Paginamos los servicios
        paginador = Paginator(servicios, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for ser in paginas:
            # Obtener observación si existe
            observacion = ''
            try:
                if hasattr(ser, 'observacion') and ser.observacion:
                    observacion = ser.observacion
            except:
                observacion = ''
            
            # Obtener rol_usuario_id si existe
            rol_usuario_id = ''
            tecnico = ''
            try:
                servicio_usuario = ServicioUsuario.objects.filter(servicio_id=ser.id).first()
                if servicio_usuario:
                    # Obtener el usuario_id del ServicioUsuario
                    usuario_id = servicio_usuario.usuario_id.id
                    rol_usuario_id = usuario_id
                    tecnico = servicio_usuario.usuario_id.username
                else:
                    print("No se encontró ServicioUsuario para este servicio")
            except Exception as e:
                print(f"Error al obtener rol_usuario_id: {e}")
                rol_usuario_id = ''
            
            data['data'].append(
                {
                    'id': ser.id,
                    'subtotal': ser.subtotal,
                    'fecha_ingreso': ser.fecha_ingreso,
                    'fecha_actualizacion': ser.fecha_actualizacion,
                    'tipo_pago': ser.tipo_pago_id.descripcion,
                    'tipo_pago_id': ser.tipo_pago_id.id,
                    'usuario_id': ser.usuario_id.username,
                    'cliente': f'{ser.cliente_id.nombres} {ser.cliente_id.apellidos}',
                    'telefono': ser.cliente_id.telefono,
                    'cliente_id': ser.cliente_id.id,
                    'tipo_servicio': ser.tipo_servicio_id.descripcion,
                    'tipo_servicio_id': ser.tipo_servicio_id.id,
                    'estado': 'Finalizado' if ser.estado else 'Abierto',
                    'estado_servicio': ser.estado,
                    'observacion': observacion,
                    'nota': ser.nota,
                    'rol_usuario_id': rol_usuario_id,
                    'tecnico': tecnico,
                    'costo_servicio': ser.costo_servicio if hasattr(ser, 'costo_servicio') else 0
                }
            )
            # Preparamos los detalles del servicio
            if len(detalle_servicio) > 0:
                for ds in detalle_servicio:
                    data['detalle_servicio'].append(
                        {
                            'id': ds.id,
                            'producto': ds.producto_id.descripcion,
                            'cantidad': ds.cantidad,
                            'precio': ds.precio,
                            'costo': ds.costo,
                            'ganancia': ds.ganancia,
                            'stock': ds.stock,
                            'total': ds.total,
                            'producto_id': ds.producto_id.id
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
        msg = 'Listado de servicios.'
    except Exception as e:
        print(f'\nSe generó un error a listar las servicios.')
        print(f'El error es: {e}\n')
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

# Endpoint para crear ticket en PDF
def ticket_pdf(request):
    servicio_id = request.GET.get('servicio_id', '')
    servicio = None
    detalle_servicio = None
    try:
        servicio = Servicio.objects.get(id=servicio_id)
    except Servicio.DoesNotExist:
        return HttpResponse("Servicio no encontrado", status=404)
    try:
        detalle_servicio = DetalleServicio.objects.filter(servicio_id = servicio_id)
    except:
        detalle_servicio = None

    
    # Tamaño para impresora térmica (80mm x altura variable)
    page_width = 80 * mm
    page_height = 300 * mm  # Altura suficiente para contenido
    custom_page_size = (page_width, page_height)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=custom_page_size, 
                           rightMargin=2*mm, leftMargin=2*mm, 
                           topMargin=2*mm, bottomMargin=2*mm)
    elements = []
    
    # Estilos personalizados
    styles = {
        'title': ParagraphStyle(
            name='Title',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            alignment=1,  # Centrado
            spaceAfter=6
        ),
        'header': ParagraphStyle(
            name='Header',
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=9,
            alignment=1,
            spaceAfter=3
        ),
        'normal': ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=7,
            leading=8,
            alignment=1,
        ),
        'small': ParagraphStyle(
            name='Small',
            fontName='Helvetica',
            fontSize=6,
            leading=7,
            alignment=1,
        ),
        'left': ParagraphStyle(
            name='Left',
            fontName='Helvetica',
            fontSize=7,
            leading=8,
            alignment=0,  # Izquierda
        ),
        'right': ParagraphStyle(
            name='Right',
            fontName='Helvetica',
            fontSize=8,
            leading=9,
            alignment=2,  # Derecha
        ),
        'center': ParagraphStyle(
            name='Center',
            fontName='Helvetica',
            fontSize=8,
            leading=9,
            alignment=1,  # Derecha
        )
    }
    
    # Encabezado de la empresa
    elements.append(Paragraph("ELECTROSISTEMAS GÓMEZ", styles['title']))
    elements.append(Paragraph("RFC: {:010}".format(servicio.id), styles['header']))
    elements.append(Paragraph("Régimen fiscal: 2046:Pequeño Contribuyente", styles['normal']))
    elements.append(Paragraph("Emitido en: Calle Al Cementario 4-14 Zona 1, Zacualpa, Quiché, ", styles['normal']))
    elements.append(Paragraph("Tel. 7736-6271", styles['normal']))
    elements.append(Spacer(1, 5))
    
    # Línea separadora
    elements.append(Paragraph("_________________________________________", styles['normal']))
    elements.append(Spacer(1, 5))
    
    # Información de cajero y fecha
    elements.append(Paragraph(f"CAJA: {servicio.usuario_id.username if (servicio.usuario_id.username != '') else 'Raymundo Gómez'}".upper(), styles['left']))
    elements.append(Paragraph(f"CLIENTE: {servicio.cliente_id.nombres} {servicio.cliente_id.apellidos}".upper(), styles['left']))
    elements.append(Paragraph(f"TIPO: {servicio.tipo_servicio_id.descripcion}".upper(), styles['left']))
    elements.append(Paragraph(f"T{servicio.id}-01322    {servicio.fecha_ingreso.strftime('%H:%M %d/%m/%Y')}", styles['left']))
    elements.append(Spacer(1, 5))
    
    # Productos (ejemplo con un producto)
    # Para múltiples productos, harías un loop aquí
    for ds in detalle_servicio:
        elements.append(Paragraph(f"{ds.producto_id.descripcion}", styles['left']))
        elements.append(
            Table([
            [
                Paragraph(f"Cant: {ds.cantidad}", styles['left']),
                Paragraph(f"Precio: {ds.precio}", styles['center']),
                Paragraph(f"Total: {ds.total}", styles['right']),
            ]
        ], colWidths=[doc.width*0.3, doc.width*0.4, doc.width*0.3]))
        elements.append(Spacer(1, 5))
    if servicio.tipo_servicio_id.id != 1:
        # En caso de servicio por mantenimiento colocar descripción
        # Línea separadora
        elements.append(Paragraph("_________________________________________", styles['normal']))
        elements.append(Spacer(1, 5))
        elements.append(
            Table([
                [
                    Paragraph(f"Costo del servicio:", styles['left']),
                    Paragraph(f"Q {servicio.costo_servicio}", styles['right'])
                ]
            ])
        )
        elements.append(
            Table([
                [
                    Paragraph(f"{servicio.observacion}", styles['center'])
                ]
            ])
        )
        elements.append(
            Table([
                [
                    Paragraph(f"{servicio.nota}", styles['center'])
                ]
            ])
        )
    
    # Totales
    #elements.append(Paragraph("1 artículo", styles['left']))
    # Línea separadora
    elements.append(Paragraph("_________________________________________", styles['normal']))
    elements.append(Spacer(1, 5))
    total_data = [
        [Paragraph("SUBTOTAL:", styles['left']), 
         Paragraph(f"Q {servicio.subtotal}", styles['right'])]
    ]
    total_table = Table(total_data, colWidths=[doc.width*0.7, doc.width*0.3])
    elements.append(total_table)
    elements.append(Spacer(1, 5))
    
    # Pago
    #elements.append(Paragraph("Pago en efectivo:    $180.00", styles['left']))
    #elements.append(Spacer(1, 10))
    
    # Términos y condiciones
    terms = "No ofrecemos cambios y devoluciones de los productos adquiridos."
    elements.append(Paragraph(terms, styles['small']))
    elements.append(Spacer(1, 10))
    
    # Información de contacto
    #elements.append(Paragraph("Visitenos en", styles['normal']))
    #elements.append(Paragraph("www.proscai.com", styles['normal']))
    #elements.append(Spacer(1, 10))
    
    # Información de facturación
    #elements.append(Paragraph("Obtenga su factura con su celular:", styles['normal']))
    #elements.append(Paragraph("También puede obtener su factura en", styles['normal']))
    #elements.append(Paragraph("www.proscai.com", styles['normal']))
    #elements.append(Paragraph("Clave para facturar: XFB ZXS NJY FTS", styles['normal']))
    #elements.append(Paragraph("Dispone de 30 días para solicitarla.", styles['normal']))
    #elements.append(Spacer(1, 10))
    
    # Pie de página
    elements.append(Paragraph("¡GRACIAS POR SU COMPRA!", styles['title']))
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
    return response

# Endpoint para crear garantía para el servicio
def garantia_servicio(request):
    if request.method == 'POST':
        # Guardamos los datos que viene por post
        observacion = request.POST.get('observacion', '').strip()
        es_perdida = request.POST.get('es_perdida', '').strip()
        servicio_id = request.POST.get('servicio_id', '').strip()
        cantidad = request.POST.get('cantidad', '').strip()
        detalle_servicio_id = request.POST.get('detalle_servicio_id', '').strip()
        garantia_id = request.POST.get('garantia_id', '').strip()
        detalle_garantia_id = request.POST.get('detalle_garantia_id', '').strip()
        print('\n--------------------------')
        print(f'observacion: {observacion}')
        print(f'es_perdida: {es_perdida}')
        print(f'servicio_id: {servicio_id}')
        print(f'cantidad: {cantidad}')
        print(f'garantia_id: {garantia_id}')
        print(f'detalle_servicio_id: {detalle_servicio_id}')
        print(f'detalle_garantia_id: {detalle_garantia_id}')
        print('--------------------------\n')
        
        # Validadmos es_perdida
        if es_perdida == 'on':
            es_perdida = True
        else:
            es_perdida = False
        # Validamos servicio_id
        if not servicio_id:
            return JsonResponse({'res': False, 'msg': 'Id servicio incorrecto.'})
        try:
            servicio_id = int(servicio_id)
        except:
            return JsonResponse({'res': False, 'msg': 'Id servicio incorrecto.'})
        # Validamos cantidad
        if not cantidad:
            cantidad = 1
        try:
            cantidad = int(cantidad)
        except:
            cantidad = 1
        if cantidad < 0:
            cantidad = 1
        # Validamos detalle_servicio_id
        if not detalle_servicio_id:
            detalle_servicio_id = None
        try:
            detalle_servicio_id = int(detalle_servicio_id)
        except:
            detalle_servicio_id = None
        # Validamos garantia_id
        if not garantia_id:
            garantia_id = None
        try:
            garantia_id = int(garantia_id)
        except:
            garantia_id = None
        # Validamos detalle_garantia_id
        if not detalle_garantia_id:
            detalle_garantia_id = None
        try:
            detalle_garantia_id = int(detalle_garantia_id)
        except Exception as error:
            print('\nERROR con detalle_garantia_id')
            print(error)
            detalle_garantia_id = None
        
        # Accedemos al servicio
        try:
            servicio = Servicio.objects.get(id = servicio_id)
        except:
            return JsonResponse({'res': False, 'msg': 'Código de servicio inválido.'})
        # Accedemos al detalle del servicio
        detalle_servicio = None
        try:
            detalle_servicio = DetalleServicio.objects.get(id = detalle_servicio_id)
        except Exception as error:
            detalle_servicio = None
        # Variables de respuestas
        msg = 'Error al crear Garantía.'
        res = False
        # Crear o editar garantía
        subtotal = 0
        try:
            garantia = Garantia.objects.update_or_create(
                id = garantia_id,
                defaults = {
                    'subtotal': subtotal,
                    'observacion': observacion,
                    'perdida': es_perdida,
                    'servicio_id': servicio,
                    'usuario_id': User.objects.get(id = request.user.id)
                }
            )
            if garantia[1]:
                msg = 'Garantía creada correctamente.'
            else:
                msg = 'Garantía actualizada correctamente.'
            res = True
        except:
            JsonResponse({'res': False, 'msg': 'Hubo un erro al crear garantía.'})
        
        if detalle_servicio_id != None:
            # Buscamos detalles de garantia con el mismo garantia_id y producto_id
            detalle_garantia = None
            try:
                detalle_garantia = DetalleGarantia.objects.filter(garantia_id = garantia_id, producto_id = detalle_servicio.producto_id.id)
                detalle_garantia_id = detalle_garantia[0].id
            except Exception as error:
                detalle_garantia_id = None
            # Verificar que la cantidad no sea mayor
            # a la cantidad que se encuentra en el detalle del serivicio
            if cantidad > detalle_servicio.cantidad:
                return JsonResponse({'res': False, 'msg': f'Sólo puedes aplicar garantía a {detalle_servicio.cantidad} productos.'})

            try:
                DetalleGarantia.objects.update_or_create(
                    id = detalle_garantia_id,
                    defaults = {
                        'precio': detalle_servicio.precio,
                        'costo': detalle_servicio.costo,
                        'cantidad': cantidad,
                        'total': cantidad * detalle_servicio.precio,
                        'producto_id': detalle_servicio.producto_id,
                        'garantia_id': garantia[0]
                    }
                )
                res = True
            except:
                JsonResponse({'res': False, 'msg': 'Hubo un error al agregar detalle de garantía'})
        # Actualizamos el subtotal de la garantía
        subtotal = sum(dg.total for dg in DetalleGarantia.objects.filter(garantia_id = garantia[0].id))
        print('\n-------------------------------')
        print(f'Subtotal: {subtotal}')
        print('-------------------------------\n')
        garantia[0].subtotal = subtotal
        garantia[0].save()

        return JsonResponse({'res': res, 'msg': msg, 'garantia_id': garantia[0].id, 'servicio_id': servicio_id})
    
# Endponint para ver garantía
def listar_garantia(request):
    # Obtenemos los datos por GET
    garantia_id = request.GET.get('garantia_id', '').strip()
    # Validar garantia_id
    if not garantia_id:
        return JsonResponse({'res': False, 'msg': 'Id de garantía inválida.'})
    try:
        garantia_id = int(garantia_id)
    except:
        return JsonResponse({'res': False, 'msg': 'Id de garantía inválida.'})
    # Accedemos al registro Garantia
    try:
        garantia = Garantia.objects.get(id = garantia_id)
    except:
        return JsonResponse({'res': False, 'msg': 'Error al acceder a la garantía'})
    # Accedemos a los detalles de la garantía
    try:
        detalle_garantia = DetalleGarantia.objects.filter(garantia_id = garantia.id)
    except:
        detalle_garantia = []
    # Accedemos a los detalles del servicio
    try:
        detalle_servicio = DetalleServicio.objects.filter(servicio_id = garantia.servicio_id.id)
    except:
        detalle_servicio = []
    # Preparamos los datos de respuesta
    data = {}
    data['dg'] = []
    data['ds'] = []
    try:
        # Preparamos los detalles del sevicio
        for ds in detalle_servicio:
            data['ds'].append(
                {
                    'detalle_servicio_id': ds.id,
                    'producto': ds.producto_id.descripcion
                }
            )
        # Preparamos los detalles de la garantía
        for dg in detalle_garantia:
            data['dg'].append(
                {
                    'garantia_id': dg.garantia_id.id,
                    'detalle_garantia_id': dg.id,
                    'precio': dg.precio,
                    'costo': dg.costo,
                    'cantidad': dg.cantidad,
                    'total': dg.total,
                    'producto_id': dg.producto_id.id,
                    'producto': dg.producto_id.descripcion,
                    'marca': dg.producto_id.marca_id.descripcion
                }
            )
        data['garantia_id'] = garantia.id
        data['subtotal'] = garantia.subtotal
        data['observacion'] = garantia.observacion
        data['perdida'] = garantia.perdida
        data['fecha_ingreso'] = garantia.fecha_ingreso
        data['servicio_id'] = garantia.servicio_id.id
        data['usuario'] = garantia.usuario_id.username
        data['res'] = True
        data['msg'] = 'Garantía obtenida.'
    except:
        data['res'] = False
        data['msg'] = 'Hubo al prepara la garantía'

    return JsonResponse(data)

# Endpoint para eliminar garantía
def eliminar_garantia(request):
    if request.method == 'POST':
        # Obtener los datos por POST
        detalle_garantia_id = request.POST.get('detalle_garantia_id', '').strip()
        garantia_id = request.POST.get('garantia_id', '').strip()

        # Validar detalle_garantia_id
        if not detalle_garantia_id:
            detalle_garantia_id = None
        try:
            detalle_garantia_id = int(detalle_garantia_id)
        except:
            detalle_garantia_id = None

        # Validar garantia_id
        if not garantia_id:
            garantia_id = None
        try:
            garantia_id = int(garantia_id)
        except:
            garantia_id = None
        
        # Eliminar detalle de garantía
        if detalle_garantia_id:
            try:
                # Obtemos el detalle de la garantía
                detalle_garantia = DetalleGarantia.objects.get(id = detalle_garantia_id)
                # Obtenemos la garantía
                garantia = detalle_garantia.garantia_id
                # Eliminamos el detalle de garantía
                detalle_garantia.delete()
                # Actualizamos el subtotal de la garantía
                subtotal = sum(dg.total for dg in DetalleGarantia.objects.filter(garantia_id = garantia.id))
                garantia.subtotal = subtotal
                garantia.save()
                return JsonResponse({'res': True, 'msg': 'Registro eliminado correctamente.'})
            except:
                return JsonResponse({'res': False, 'msg': 'Error al eliminar registro.'})
            
        # Eliminar garantía completa
        if garantia_id:
            try:
                Garantia.objects.get(id = garantia_id).delete()
                return JsonResponse({'res': True, 'msg': 'Registro eliminado correctamente.'})
            except:
                return JsonResponse({'res': False, 'msg': 'Error al eliminar registro.'})
        return JsonResponse({'res': False, 'msg': 'Método no permitido.'})