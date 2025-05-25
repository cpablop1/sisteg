from django.shortcuts import render
from django.http import JsonResponse

from django.core.paginator import Paginator

from django.db.models import Q
from django.contrib.auth.models import User

from .models import Categoria, Marca

#Función para renderizar la vista de producto
def vista_producto(request):
    return render(request, 'producto/producto.html')

#Función para renderizar la vista de categoria
def vista_categoria(request):
    return render(request, 'categoria/categoria.html')

#Función para renderizar la vista de marca
def vista_marca(request):
    return render(request, 'marca/marca.html')

# Función para agregar categoría
def agregar_categoria(request):
    # Mensaje de respuesta
    res = False
    msg = '¡Método no permitido!'
    # Evaluamos si es llamado por POST
    if request.method == 'POST':
        # Capturamos los métodos por POST
        id = request.POST.get('id', None) or None
        descripcion = request.POST.get('descripcion', None).strip().upper() or ''
        # Creamos la categoría
        try:
            categoria = Categoria.objects.update_or_create(
                id = id,
                defaults = {
                    'descripcion': descripcion,
                    'usuario_id': User.objects.get(id = request.user.id)
                }
            )
            res = True
            # Evaluamos si fue un nuevo registro o una actualización
            if categoria[1]:
                msg = 'Categoría agregada correctamente.'
            else:
                msg = 'Categoría actualizada correctamente.'
        except:
            res = False
            msg = 'Hubo un error al agregar categoría, actualice la página y vuleve a intentarlo.'
        # Retornamos una respuesta de éxito
        return JsonResponse({'res': res, 'msg': msg})
    else: # En caso contrario
        # Retornamos una respuesta de error
        return JsonResponse({'res': res, 'msg': msg})
    
# Función para listar categorías
def listar_categoria(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar categorías.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    categorias = ''

    try:
        if id: # Verificamos si necesitamos una categoría expecífica
            categorias = Categoria.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            categorias = Categoria.objects.filter(
                Q(descripcion__icontains = buscar) # Si hay buscamos por descripción
            )
        else:
            # Obtenemos todas las categorías
            categorias = Categoria.objects.all()
        # Paginamos las categorías
        paginador = Paginator(categorias, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for cat in paginas:
            data['data'].append(
                {
                    'id': cat.id,
                    'descripcion': cat.descripcion,
                    'fecha_ingreso': cat.fecha_ingreso,
                    'fecha_actualizacion': cat.fecha_actualizacion,
                    'usuario': cat.usuario_id.username
                }
            )
        # Preparamos la visualización de las páginas
        if paginador.num_pages > 5:
            print('\n-----------------')
            print(paginador.num_pages)
            print('-----------------\n')
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
        msg = 'Listado de categorías.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

# Función para agregar marca
def agregar_marca(request):
    # Mensaje de respuesta
    res = False
    msg = '¡Método no permitido!'
    # Evaluamos si es llamado por POST
    if request.method == 'POST':
        # Capturamos los métodos por POST
        id = request.POST.get('id', None) or None
        descripcion = request.POST.get('descripcion', None).strip().upper() or ''
        # Creamos la marca
        try:
            marca = Marca.objects.update_or_create(
                id = id,
                defaults = {
                    'descripcion': descripcion,
                    'usuario_id': User.objects.get(id = request.user.id)
                }
            )
            res = True
            # Evaluamos si fue un nuevo registro o una actualización
            if marca[1]:
                msg = 'Marca agregada correctamente.'
            else:
                msg = 'Marca actualizada correctamente.'
        except:
            res = False
            msg = 'Hubo un error al agregar marca, actualice la página y vuleve a intentarlo.'
        # Retornamos una respuesta de éxito
        return JsonResponse({'res': res, 'msg': msg})
    else: # En caso contrario
        # Retornamos una respuesta de error
        return JsonResponse({'res': res, 'msg': msg})

# Función para listar marcas
def listar_marca(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar marcas.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    marcas = ''

    try:
        if id: # Verificamos si necesitamos una marca expecífica
            marcas = Marca.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            marcas = Marca.objects.filter(
                Q(descripcion__icontains = buscar) # Si hay buscamos por descripción
            )
        else:
            # Obtenemos todas las marcas
            marcas = Marca.objects.all()
        # Paginamos las marcas
        paginador = Paginator(marcas, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for mar in paginas:
            data['data'].append(
                {
                    'id': mar.id,
                    'descripcion': mar.descripcion,
                    'fecha_ingreso': mar.fecha_ingreso,
                    'fecha_actualizacion': mar.fecha_actualizacion,
                    'usuario': mar.usuario_id.username
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
        msg = 'Listado de marcas.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)