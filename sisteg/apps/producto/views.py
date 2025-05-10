from django.shortcuts import render

def vista_producto(request):
    return render(request, 'producto/producto.html')