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

from .models import Cliente, Servicio, DetalleServicio, TipoServicio
from apps.producto.models import Producto
from apps.inicio.models import TipoPago

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
        cliente_id = request.POST.get('cliente_id', '').strip()
        tipo_pago_id = request.POST.get('tipo_pago_id', '').strip()
        producto_id = request.POST.get('producto_id', '').strip()
        tipo_servicio_id = request.POST.get('tipo_servicio_id', '').strip()
        cantidad = request.POST.get('cantidad', '1')
        print('\n----------------------------------')
        print(f'Cliente: {cliente_id}')
        print(f'Tipo pago: {tipo_pago_id}')
        print(f'Producto: {producto_id}')
        print(f'Cantidad: {cantidad}')
        print(f'Rol usuario: {request.rol_usuario}')
        print('----------------------------------\n')

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
            # Verificamos si existe una venta activa del usuario logeado
            existe_servicio = Servicio.objects.filter(usuario_id = request.user.id, estado = False)
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
                        total = total
                    )
                else: # En caso contrario agregar el producto al carrito (venta)
                    detalle = DetalleServicio.objects.create(
                        costo = producto.costo,
                        cantidad = cantidad,
                        total = producto.costo,
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
                    subtotal = producto.costo,
                    cliente_id = Cliente.objects.get(id = cliente_id),
                    usuario_id = User.objects.get(id = request.user.id),
                    tipo_pago_id = TipoPago.objects.get(id = tipo_pago_id),
                    tipo_servicio_id = TipoServicio.objects.get(id = tipo_servicio_id)
                )
                # Con su detalle
                detalle_servicio = DetalleServicio.objects.create(
                    costo = producto.costo,
                    cantidad = cantidad,
                    total = producto.costo,
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