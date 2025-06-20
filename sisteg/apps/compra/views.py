from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import Proveedor

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