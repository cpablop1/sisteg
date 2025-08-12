from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import RolUsuario

def vista_autenticacion(request):
    return render(request, 'autenticacion/login.html')

# Funcionalidad para iniciar sesión
def iniciar(request):
    res = False
    msg = 'Método inválido.'
    if request.method == 'POST':
        # Recogemos los datos por POST
        usuario = request.POST.get('usuario', '') or ''
        clave = request.POST .get('clave', '') or ''

        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            res = True
            msg = 'Autenticación exitosa.'
        else:
            res = False
            msg = 'Ingrese una contraseña y usuario válido.'

    return JsonResponse({'res': res, 'msg': msg})

# Funcionalidad para cerrar sesión
def cerrar (request):
    logout(request)
    return redirect('autenticacion')

# Función para listar usuarios por roles
@login_required(login_url='autenticacion')
def listar_rol_usuario(request):
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar usuarios por rol.'
    data = {}
    data['data'] = []
    id = request.GET.get('id', None) or None
    rol_usuario = ''

    try:
        if id: # Verificamos si necesitamos un rol usuario en expecífico
            rol_usuario = RolUsuario.objects.filter(id = id)
        else:
            # Obtenemos todas los roles usuarios
            rol_usuario = RolUsuario.objects.all()
            
        # Preparamos el listado
        for ru in rol_usuario:
            if ru.rol_id.rol != 'recepcionista':
                data['data'].append(
                    {
                        'usuario_id': ru.usuario_id.id,
                        'usuario': ru.usuario_id.username,
                        'rol': ru.rol_id.rol
                    }
                )

        # Preparamos mensajes de respuesta
        res = True
        msg = 'Listado de roles usuarios.'
    except:
        res = False

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)