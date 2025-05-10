from django.shortcuts import render

def vista_autenticacion(request):
    return render(request, 'autenticacion/autenticacion.html')