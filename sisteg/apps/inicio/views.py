from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import TipoPago
from apps.compra.models import Compra
from apps.servicio.models import Servicio, Garantia, TipoServicio
from apps.producto.models import Producto

@login_required(login_url='autenticacion')
def vista_inicio(request):
    return render(request, 'inicio/inicio.html')

@login_required(login_url='autenticacion')
def listar_tipo_pago(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar tipos de pagos.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    select = request.GET.get('select', None) or None
    tipo_pago = ''

    try:
        if id: # Verificamos si necesitamos una categoría expecífica
            tipo_pago = TipoPago.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsquedad
            tipo_pago = TipoPago.objects.filter(
                Q(descripcion__icontains = buscar) # Si hay buscamos por descripción
            )
        else:
            # Obtenemos todas las categorías
            tipo_pago = TipoPago.objects.all()
            
        if select:
            paginas = tipo_pago
        else:
            # Paginamos las categorías
            paginador = Paginator(tipo_pago, 10)
            # Obtenemos la página
            paginas = paginador.get_page(pagina)
            # Preparamos el listado
        for tip in paginas:
            data['data'].append(
                {
                    'id': tip.id,
                    'descripcion': tip.descripcion,
                    'fecha_ingreso': tip.fecha_ingreso,
                    'fecha_actualizacion': tip.fecha_actualizacion,
                    'usuario': tip.usuario_id.username
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
        msg = 'Listado de listado de tipo de pagos.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)

def estadistica(request):
    compra = ''
    servicio = ''
    producto  = ''
    data = {}
    data['compra'] = []
    data['servicio'] = []
    data['grafica'] = []

    try:
        # Preparamos los datos de compra
        compra = Compra.objects.all()
        total = sum(co.subtotal for co in compra)
        cantidad = compra.count()
        data['compra'].append({
            'total': f'Q {total} en compras',
            'cantidad': f'{cantidad} realizadas'
        })
        # Preparamos los datos de servicio
        tipo_servicio = TipoServicio.objects.all()
        for tp in tipo_servicio:
            servicio = Servicio.objects.filter(tipo_servicio_id = tp.id)
            total = sum(ser.subtotal for ser in servicio)
            cantidad = servicio.count()
            data['servicio'].append({
                'tipo_servicio': tp.descripcion,
                'total': f'Q {total} en {tp.descripcion}',
                'cantidad': f'{cantidad} realizadas'
            })
        # Preparamos los datos para la gráfica
        for tp in tipo_servicio:
            servicio = Servicio.objects.filter(tipo_servicio_id = tp.id)
            cantidad = servicio.count()
            data['grafica'].append({
                'descripcion': tp.descripcion,
                'cantidad': cantidad
            })
    except:
        pass

    return JsonResponse(data)