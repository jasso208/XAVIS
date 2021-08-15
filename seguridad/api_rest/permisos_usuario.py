from seguridad.services.usuario import UsuarioService
from rest_framework.response import Response
from rest_framework.views import APIView
from seguridad.models.user_2 import User_2
from seguridad.models.permisos_usuario import Permisos_Usuario
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.models import User
from seguridad.models.menu import Menu
class PermisosUsuarioApi(APIView):
    #parametros
    #               token: El token del usuario que esta logueado
    #               tipo_accion: 
    #                               vacio es para obtener todos los permisos del usuario (validamos por token); 
    #                               "1" para validar si el usuario tiene acceso a una vista en particular
    #                               "2" para obtener todos los permisos del usuario (validamos por username)              
    #               id_opcion: <opcional> Es el id de la opcion a la que se le validara el permiso
    #return 
    #               Regresa todas las opciones a las que tiene acceso el usuario.
    def get(self,request,format = None):
        token = request.GET.get("token")
        username = request.GET.get("username")
        tipo_accion = request.GET.get("tipo_accion")
        id_opcion = request.GET.get("id_opcion")
        print(tipo_accion)
        if tipo_accion == "2":#validamos por username
            usuario = User.objects.get(username = username)
        else: #validamos por token
            usuario = Token.objects.get(key = token).user

        if tipo_accion == "1":
            return Response(json.dumps(Permisos_Usuario.validaAccesoAVista(usuario,id_opcion)))
        else:
            return Response(Permisos_Usuario.getPermisos(usuario))
    #recibe el username y la opcion que se desea agregar o quitar.
    #Parametros
    #           user_name
    #           id_opcion
    #           accion: true: agregams permiso; false: quitamos el permiso.
    def put(self,request,format = None):
        user_name  =request.data["user_name"]
        id_opcion = request.data["id_opcion"]
        accion = request.data["accion"]
        token = request.data["token"]

        opcion = Menu.objects.get(id = id_opcion)
        user = User.objects.get(username = user_name)
        usuario_otorga = Token.objects.get(key = token).user

        return Response(UsuarioService.editaPermisosUsuario(user,opcion,accion,usuario_otorga))
