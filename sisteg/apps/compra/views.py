from django.shortcuts import render

def vista_compra(request):
    return render(request, 'compra/compra.html')