from rest_framework.response import Response
from seguridad.models.perfil import Perfil
from django.http import JsonResponse
from rest_framework.views import APIView
from seguridad.serializers.perfil_serializer import PerfilSerializer
import json
from django.db.models.functions import Upper
from seguridad.services.perfil import PerfilService
from seguridad.models.menu import Menu
class PerfilApi(APIView):
    #obtiene todos los perfiles o uno en particular, dependiendo el parametro tipo de busqueda.
    #parametros:
    #           tipo_busqueda: 1 para todos los perfiles; 2 para buscar un solo perfil
    #           id_perfil:Opcional: es el id de perfil que vamos a buscar, solo para perfiles
    def get(self,request,format = None):

        tipo_busqueda = request.GET.get("tipo_busqueda")
        id_perfil = request.GET.get("id_perfil")

        if tipo_busqueda == "1":
            respuesta = PerfilSerializer(Perfil.obtenerTodosPerfiles(),many = True)
            return JsonResponse(respuesta.data,safe = False)
        elif tipo_busqueda == "2":
            perfil = Perfil.objects.get(id = id_perfil)
            return Response(PerfilService.getPermisosPorPerfil(perfil))
            
        return Response("")
        

    #parametros:
    #               tipo_accion: indica el tipo de acccion: 1 para alta de perfl
    def post(self,request,format = None):
        perfil = request.data["perfil"]
        comentarios = request.data["comentarios"]
        tipo_accion = request.data["tipo_accion"]

        resp = {}
        if tipo_accion == "1":
                        
            try:
                Perfil.objects.create(perfil = perfil.upper(),comentarios = comentarios.upper())
                resp = {"estatus":"1"}
            except Exception as e:
                resp = {"estatus":"0","msj":"Error al crear el perfil."}

        return Response(json.dumps(resp))

    #recibe el perfil y la opcion que se desea agregar o quitar.
    #Parametros
    #           id_perfil
    #           id_opcion
    #           accion: true: agregams permiso; false: quitamos el permiso.
    def put(self,request,format=None):
        id_perfil  =request.data["id_perfil"]
        id_opcion = request.data["id_opcion"]
        accion = request.data["accion"]

        opcion = Menu.objects.get(id = id_opcion)
        perfil = Perfil.objects.get(id = id_perfil)

        return Response(PerfilService.editaPermisosPerfil(perfil,opcion,accion))

