from rest_framework.response import Response
from rest_framework.views import APIView
from seguridad.models.user_2 import User_2
from seguridad.models.permisos_usuario import Permisos_Usuario
from rest_framework.authtoken.models import Token
import json
class UsuarioApi(APIView):
    #parametros
    #               token: El token del usuario que esta logueado
    #               tipo_accion: vacio es para obtener todos los permisos; 1 para validar si el usuario tiene acceso a una vista en particular
    #               id_opcion: <opcional> Es el id de la opcion a la que se le validara el permiso
    #return 
    #               Regresa todas las opciones a las que tiene acceso el usuario.
    def get(self,request,format = None):
        token = request.GET.get("token")
        tipo_accion = request.GET.get("tipo_accion")
        id_opcion = request.GET.get("id_opcion")
        usuario = Token.objects.get(key = token).user
        if tipo_accion == "1":
            return Response(json.dumps(Permisos_Usuario.validaAccesoAVista(usuario,id_opcion)))
        else:
            return Response(Permisos_Usuario.getPermisos(usuario))

