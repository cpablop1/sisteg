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

from .models import Cliente
from apps.producto.models import Producto
from apps.inicio.models import TipoPago

@login_required(login_url='autenticacion')
def vista_cliente(request):
    return render(request, 'cliente/cliente.html')

def vista_servicio(request):
    return render(request, 'servicio/servicio.html')

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