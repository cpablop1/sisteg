from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.db import transaction, IntegrityError, connection
from django.db.models import F
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from apps.producto.models import Producto
from apps.inicio.models import TipoPago

@login_required(login_url='autenticacion')
def vista_cliente(request):
    return render(request, 'cliente/cliente.html')

def vista_servicio(request):
    return render(request, 'servicio/servicio.html')