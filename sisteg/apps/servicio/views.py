from django.shortcuts import render

def vista_servicio(request):
    return render(request, 'servicio/servicio.html')