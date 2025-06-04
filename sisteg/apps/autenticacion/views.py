from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def vista_autenticacion(request):
    return render(request, 'autenticacion/login.html')

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