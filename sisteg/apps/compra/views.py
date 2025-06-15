from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User

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