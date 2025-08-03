from apps.autenticacion.models import RolUsuario

class GlobalDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                #request.user_role = request.user.role  # Asigna al request
                usuario_id = request.user.id # Obtenemos el id del usuario autenticado
                rol = RolUsuario.objects.get(usuario_id = usuario_id) # Luego obtenemos el rol del usuario autenticado
                request.rol_usuario = rol.rol_id.rol  # Asigna al request
            except:
                request.rol_usuario = 'Sin rol'
        else:
            request.rol_usuario = 'Sin rol'
        return self.get_response(request)