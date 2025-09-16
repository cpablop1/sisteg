from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import RolUsuario, Rol
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

def vista_autenticacion(request):
    """
    Vista para mostrar el formulario de autenticación.
    
    Esta vista renderiza la página de login donde los usuarios pueden
    iniciar sesión en el sistema.
    
    Args:
        request: Objeto HttpRequest que contiene los datos de la petición.
        
    Returns:
        HttpResponse: Renderiza el template 'autenticacion/login.html'.
    """
    return render(request, 'autenticacion/login.html')

def vista_usuario(request):
    """
    Vista para mostrar la página de gestión de usuarios.
    
    Esta vista renderiza la página donde se pueden gestionar
    los usuarios del sistema, incluyendo la creación, edición
    y listado de usuarios.
    
    Args:
        request: Objeto HttpRequest que contiene los datos de la petición.
        
    Returns:
        HttpResponse: Renderiza el template 'usuario/usuario.html'.
    """
    return render(request, 'usuario/usuario.html')

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

# Funcion para agregar/editar usuario
@login_required(login_url='autenticacion')
def agregar_usuario(request):
    """
    Crea o actualiza un usuario a partir de datos enviados por POST.

    Para crear: 'username', 'password' y 'rol' son requeridos.
    Para editar: 'id' del usuario existente, 'username' y 'rol' son requeridos.
    Opcionales: 'email', 'first_name', 'last_name'.

    Retorna un JsonResponse con 'res' (bool) y 'msg' (str).
    """
    res = False
    msg = 'Método inválido.'

    if request.method == 'POST':
        user_id = request.POST.get('id', None)
        username = (request.POST.get('username') or '').strip()
        password = (request.POST.get('password') or '').strip()
        email = (request.POST.get('email') or '').strip()
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        rol = (request.POST.get('rol') or '').strip()

        # Validaciones básicas
        if not username or not rol:
            msg = 'Username y rol son requeridos.'
            return JsonResponse({'res': res, 'msg': msg})

        # Si es edición, password no es requerido
        if not user_id and not password:
            msg = 'Password es requerido para crear un nuevo usuario.'
            return JsonResponse({'res': res, 'msg': msg})

        try:
            # Verificar si el username ya existe (excepto si es el mismo usuario)
            existing_user = User.objects.filter(username=username)
            if user_id:
                existing_user = existing_user.exclude(id=user_id)
            
            if existing_user.exists():
                msg = 'El nombre de usuario ya existe.'
                return JsonResponse({'res': res, 'msg': msg})

            # Obtener el rol
            try:
                rol_obj = Rol.objects.get(rol=rol, estado=True)
            except Rol.DoesNotExist:
                msg = 'El rol seleccionado no es válido.'
                return JsonResponse({'res': res, 'msg': msg})

            if user_id:  # Editar usuario existente
                try:
                    user = User.objects.get(id=user_id)
                    user.username = username
                    user.email = email or None
                    user.first_name = first_name
                    user.last_name = last_name
                    
                    # Solo actualizar password si se proporciona
                    if password:
                        user.set_password(password)
                    
                    user.save()

                    # Actualizar rol
                    rol_usuario, created = RolUsuario.objects.update_or_create(
                        usuario_id=user,
                        defaults={'rol_id': rol_obj}
                    )

                    res = True
                    msg = 'Usuario actualizado correctamente.'
                except User.DoesNotExist:
                    msg = 'Usuario no encontrado.'
                    return JsonResponse({'res': res, 'msg': msg})
            else:  # Crear nuevo usuario
                user = User.objects.create_user(
                    username=username,
                    email=email or None,
                    password=password,
                )
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = True
                user.save()

                # Crear relación RolUsuario
                RolUsuario.objects.create(
                    usuario_id=user,
                    rol_id=rol_obj
                )

                res = True
                msg = 'Usuario creado correctamente.'

        except Exception as e:
            res = False
            msg = f'Error al procesar usuario: {e}'

    return JsonResponse({'res': res, 'msg': msg})


# Funcion para listar solo los roles disponibles
@login_required(login_url='autenticacion')
def listar_roles(request):
    """
    Lista todos los roles disponibles en el sistema.
    
    Retorna un JsonResponse con los roles activos que pueden ser asignados a usuarios.
    
    Returns:
        JsonResponse: {'res': bool, 'msg': str, 'data': list}
    """
    try:
        roles = Rol.objects.filter(estado=True).values('id', 'rol')
        return JsonResponse({
            'res': True, 
            'msg': 'Roles listados correctamente.', 
            'data': list(roles)
        })
    except Exception as e:
        return JsonResponse({
            'res': False, 
            'msg': f'Error al listar roles: {e}', 
            'data': []
        })

# Funcion para listar usuarios con sus roles (para ventas)
@login_required(login_url='autenticacion')
def listar_usuarios_con_roles(request):
    """
    Lista todos los usuarios con sus roles asignados.
    
    Esta función es específica para el módulo de ventas donde se necesita
    mostrar tanto el rol como el nombre del usuario.
    
    Returns:
        JsonResponse: {'res': bool, 'msg': str, 'data': list}
    """
    try:
        # Obtener usuarios con roles asignados, excluyendo recepcionistas
        usuarios_con_roles = RolUsuario.objects.select_related('usuario_id', 'rol_id').filter(
            rol_id__estado=True
        ).exclude(
            rol_id__rol='recepcionista'
        ).values(
            'usuario_id',
            'usuario_id__username',
            'usuario_id__first_name',
            'usuario_id__last_name',
            'rol_id__rol'
        )
        
        data = []
        for item in usuarios_con_roles:
            # Formatear nombre completo
            nombre_completo = f"{item['usuario_id__first_name']} {item['usuario_id__last_name']}".strip()
            if not nombre_completo:
                nombre_completo = item['usuario_id__username']
            
            data.append({
                'usuario_id': item['usuario_id'],
                'username': item['usuario_id__username'],
                'nombre_completo': nombre_completo,
                'rol': item['rol_id__rol']
            })
        
        return JsonResponse({
            'res': True, 
            'msg': 'Usuarios con roles listados correctamente.', 
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'res': False, 
            'msg': f'Error al listar usuarios con roles: {e}', 
            'data': []
        })
    
# Funcion para listar Usuario
@login_required(login_url='autenticacion')
def listar_usuario(request):
    """
    Lista todos los usuarios con paginación.
    
    Retorna un JsonResponse con los usuarios paginados, incluyendo información
    de paginación y búsqueda.
    
    Returns:
        JsonResponse: {'res': bool, 'msg': str, 'data': list, 'page_range': list, 
                      'num_pages': int, 'has_next': bool, 'has_previous': bool, 'count': int}
    """
    
    # Mensajes de respuesta
    res = False
    msg = 'Error al listar usuarios.'
    data = {}
    data['data'] = []
    data["page_range"] = []
    
    # Parámetros de consulta
    id = request.GET.get('id', None) or None
    buscar = request.GET.get('buscar', '').strip() or ''
    pagina = request.GET.get('pagina', 1) or 1
    select = request.GET.get('select', None) or None
    usuarios = ''

    try:
        if id: # Verificamos si necesitamos un usuario específico
            usuarios = User.objects.filter(id = id)
        elif len(buscar) > 0: # Verificamos si hay búsqueda
            usuarios = User.objects.filter(
                Q(username__icontains = buscar) | # Buscamos por nombre de usuario
                Q(first_name__icontains = buscar) | # Buscamos por nombre
                Q(last_name__icontains = buscar) | # Buscamos por apellido
                Q(email__icontains = buscar) # Buscamos por email
            )
        else:
            # Obtenemos todos los usuarios
            usuarios = User.objects.all()
            
        if select:
            paginas = usuarios
        else:
            # Paginamos los usuarios
            paginador = Paginator(usuarios, 10)
            # Obtenemos la página
            paginas = paginador.get_page(pagina)
            
        # Preparamos el listado
        for user in paginas:
            # Obtener el rol del usuario si existe
            try:
                rol_usuario = RolUsuario.objects.get(usuario_id=user)
                rol = rol_usuario.rol_id.rol
            except RolUsuario.DoesNotExist:
                rol = 'Sin rol'
            
            data['data'].append(
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'date_joined': user.date_joined,
                    'last_login': user.last_login,
                    'rol': rol
                }
            )
            
        # Preparamos la visualización de las páginas
        if not select:
            if paginador.num_pages > 5:
                start = int(pagina)
                end = int(pagina) + 5
                if end > paginador.num_pages:
                    start = paginador.num_pages - 4
                    end = paginador.num_pages + 1
                for i in range(start, end):
                    data["page_range"].append(i)
            else:
                for i in range(paginador.num_pages):
                    data["page_range"].append(i + 1)
            data["num_pages"] = paginador.num_pages
            data["has_next"] = paginas.has_next()
            data["has_previous"] = paginas.has_previous()
            data["count"] = paginador.count

        # Preparamos mensajes de respuesta
        res = True
        msg = 'Listado de usuarios.'
    except Exception as e:
        res = False
        msg = f'Error al listar usuarios: {str(e)}'

    data['res'] = res
    data['msg'] = msg
    # Retornamos los datos
    return JsonResponse(data)