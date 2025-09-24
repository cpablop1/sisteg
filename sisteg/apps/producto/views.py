from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.db.models import Q
from django.contrib.auth.models import User

from .models import Categoria, Marca, Producto

#Función para renderizar la vista de producto
@login_required(login_url='autenticacion')
def vista_producto(request):
    return render(request, 'producto/producto.html')

#Función para renderizar la vista de categoria
@login_required(login_url='autenticacion')
def vista_categoria(request):
    return render(request, 'categoria/categoria.html')

#Función para renderizar la vista de marca
@login_required(login_url='autenticacion')
def vista_marca(request):
    return render(request, 'marca/marca.html')

# Función para agregar categoría
@login_required(login_url='autenticacion')
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
@login_required(login_url='autenticacion')
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
    select = request.GET.get('select', None) or None
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
            
        if select:
            paginas = categorias
        else:
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
@login_required(login_url='autenticacion')
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
@login_required(login_url='autenticacion')
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
    select = request.GET.get('select', None) or None
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
        if select:
            paginas = marcas
        else:
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

# Funcionalidad para crear productos
@login_required(login_url='autenticacion')
def agregar_producto(request):
    if request.method == 'POST':
        # Recoger los datos por POST
        id = request.POST.get("id", None) or None
        descripcion = request.POST.get("descripcion", '').strip().upper() or ''
        detalle = request.POST.get("detalle", '').strip() or ''
        costo = request.POST.get("costo", 0).strip() or 0
        precio = request.POST.get("precio", 0).strip() or 0
        stock = request.POST.get("stock", 0).strip() or 0
        img1 = request.FILES.get('img1', None) or None
        img2 = request.FILES.get('img2', None) or None
        marca_id = request.POST.get("marca_id", None).strip() or None
        categoria_id = request.POST.get("categoria_id", None).strip() or None
        usuario_id = User.objects.get(id=request.user.id)
        eliminar_img1 = request.POST.get('eliminar_img1')
        eliminar_img2 = request.POST.get('eliminar_img2')
        
        data = {
            "descripcion": descripcion,
            "detalle": detalle,
            "costo": costo,
            "precio": precio,
            "stock": stock,
            "marca_id": Marca.objects.get(id=marca_id),
            "categoria_id": Categoria.objects.get(id=categoria_id),
        }
        # Ver si hay imáganes que agregar
        if img1 != None:
            data['img1'] = img1

        if img2 != None:
            data['img2'] = img2

        # Ver si hay imágenes que borrar
        if eliminar_img1 != None and id != None:
            data['img1'] = ''
        
        if eliminar_img2 != None and id != None:
            data['img2'] = ''
        
        # Ver si es necesario agregar el usuario y oficina
        if id == None:
            data['usuario_id'] = usuario_id

        try:
            producto = Producto.objects.update_or_create(
                id=id,
                defaults=data
            )
            if producto[1]:
                return JsonResponse({"res": True, "msg": "Producto registrado correctamente."})
            else:
                return JsonResponse({"res": True, "msg": "Producto actualizado correctamente."})
        except:
            return JsonResponse({"res": False, "msg": "¡Hubo un error al registrar producto!"})

# Función para listar productos
@login_required(login_url='autenticacion')
def listar_producto(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar productos.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    productos = ''

    try:
        if id: # Verificamos si necesitamos un producto expecífica
            productos = Producto.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            productos = Producto.objects.filter(
                Q(descripcion__icontains = buscar) # Si hay buscamos por descripción
            )
        else:
            # Obtenemos todas los productos
            productos = Producto.objects.all()
        # Paginamos los productos
        paginador = Paginator(productos, 10)
        # Obtenemos la página
        paginas = paginador.get_page(pagina)
        # Preparamos el listado
        for pro in paginas:
            data['data'].append(
                {
                    'id': pro.id,
                    'descripcion': pro.descripcion,
                    'detalle': pro.detalle,
                    'costo': pro.costo,
                    'precio': pro.precio,
                    'stock': pro.stock,
                    'img1': pro.img1.name,
                    'img2': pro.img2.name,
                    'fecha_ingreso': pro.fecha_ingreso,
                    'fecha_actualizacion': pro.fecha_actualizacion,
                    'marca_id': pro.marca_id.id,
                    'categoria_id': pro.categoria_id.id,
                    'marca': pro.marca_id.descripcion,
                    'categoria': pro.categoria_id.descripcion,
                    'usuario': pro.usuario_id.username
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
        msg = 'Listado de productos.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)