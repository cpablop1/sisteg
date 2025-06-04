from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='iniciar')
def vista_inicio(request):
    return render(request, 'inicio/inicio.html')