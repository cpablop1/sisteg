from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

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