from rest_framework.response import Response
from seguridad.models.perfil import Perfil
from django.http import JsonResponse
from rest_framework.views import APIView
from seguridad.serializers.perfil_serializer import PerfilSerializer
import json
class PerfilApi(APIView):
    #obtiene todos los perfiles o uno en particular, dependiendo el parametro tipo de busqueda.
    #parametros:
    #           tipo_busqueda: 1 para todos los perfiles; 2 para buscar un solo perfil
    #           id_perfil:Opcional: es el id de perfil que vamos a buscar, solo para perfiles
    def get(self,request,format = None):

        tipo_busqueda = request.GET.get("tipo_busqueda")
        
        if tipo_busqueda == "1":
            respuesta = PerfilSerializer(Perfil.obtenerTodosPerfiles(),many = True)
        else:
            respuesta = PerfilSerializer(Perfil.obtenerTodosPerfiles(),many = True)
        
        return JsonResponse(respuesta.data,safe = False)

    #parametros:
    #               tipo_accion: indica el tipo de acccion: 1 para alta de perfl
    def post(self,request,format = None):
        perfil = request.data["perfil"]
        comentarios = request.data["comentarios"]
        tipo_accion = request.data["tipo_accion"]

        resp = {}
        if tipo_accion == "1":
                        
            try:
                Perfil.objects.create(perfil = perfil,comentarios = comentarios)
                resp = {"estatus":"1"}
            except:
                resp = {"estatus":"0","msj":"Error al crear el perfil."}

        return Response(json.dumps(resp))