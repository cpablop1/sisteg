from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='autenticacion')
def vista_compra(request):
    return render(request, 'compra/compra.html')

@login_required(login_url='autenticacion')
def vista_proveedor(request):
    return render(request, 'proveedor/proveedor.html')