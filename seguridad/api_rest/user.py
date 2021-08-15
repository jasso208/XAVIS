
from rest_framework.response import Response
from rest_framework.views import APIView
from seguridad.services.usuario import UsuarioService
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
class UsuarioApi(APIView):
    #para obtener informacion del usuario
    #parametros
    #           tipo_accion: 0: todos los usuarios; 1: consulta un solo usuario    
    #           id_usuario: El usuario que deseamos consultar
    def get(self,request,format=None):
        tipo_accion = request.GET.get("tipo_accion")
        id_usuario = request.GET.get("id_usuario")
        if tipo_accion == "0":
            return Response(UsuarioService.consultaListaUsuarios())
        elif tipo_accion=="1":
            return Response(UsuarioService.consultaUsuarioPorId(id_usuario))
        return Response("")

    #alta de usuario:
    #parametros:
    #           tipo_accion: 1 para alta de usuario
    #           user_name,
    #           first_name,
    #           last_name,
    #           id_sucursal,
    #           id_perfil,
    #           token,              token del usuario que registra
    #           email
    #respuesta(diccionario)
    #           estatus: 0 Error al guardar el usuario; 1: Se guardo correctamente.
    #           msj: <opcional> Solo en caso de marcar error, manda el motivo del porque marco error
    def post(self,request,format=None):
        resp = {}
        tipo_accion = request.data["tipo_accion"]
        user_name = request.data["user_name"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        id_sucursal = request.data["id_sucursal"]
        id_perfil = request.data["id_perfil"]
        token = request.data["token"]
        email = request.data["email"]

        if tipo_accion == 1:
            usuario = Token.objects.get(key = token).user
            resp = UsuarioService.fn_alta_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,usuario.id,email)
            if resp[0]:
                resp = {"estatus":"1"}
            else:
                resp = {"estatus":"0","msj":resp[1]}
            
        return Response(resp)

    #actualizacion de usuario
    #Parametros:
    #               id_usuario
    #               user_name
    #               first_name
    #               last_name
    #               id_sucursal
    #               id_perfil
    #               token
    #               email
    def put(self,request,format=None):
        user_name  = request.data["user_name"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        id_sucursal = request.data["id_sucursal"]
        id_perfil = request.data["id_perfil"]
        token = request.data["token"]
        email = request.data["email"]
        activo = request.data["activo"]
        try:
            user_edita = Token.objects.get(key = token).user
        except:
            return Response({"estatus":"0","msj":"Inicie sesion para realizar esta acción."})    

        res = UsuarioService.fn_edita_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,user_edita.id,activo,email)
        resp = {}
        if res[0]:
            resp = {"estatus":"1"}
        else:
            resp = {"estatus":"0","msj":res[1]}
        return Response(resp)


