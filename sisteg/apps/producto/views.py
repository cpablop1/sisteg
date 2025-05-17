from django.shortcuts import render
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User

from .models import Categoria

#Función para renderizar la vista de producto
def vista_producto(request):
    return render(request, 'producto/producto.html')

#Función para renderizar la vista de categoria
def vista_categoria(request):
    return render(request, 'categoria/categoria.html')

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
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''

    try:
        if id: # Verificamos si necesitamos una categoría expecífica
            categorias = Categoria.objects.filter(id = id)
        elif len(buscar) > 0:
            categorias = Categoria.objects.filter(
                Q(descripcion__icontains = buscar)
            )
        else:
            # Obtenemos todas las categorías
            categorias = Categoria.objects.all()
        # Preparamos el listado
        for cat in categorias:
            data['data'].append(
                {
                    'id': cat.id,
                    'descripcion': cat.descripcion,
                    'fecha_ingreso': cat.fecha_ingreso,
                    'fecha_actualizacion': cat.fecha_actualizacion,
                    'usuario': cat.usuario_id.username
                }
            )
        res = True
        msg = 'Listado de categorías.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)