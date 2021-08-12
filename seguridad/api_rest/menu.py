from rest_framework.response import Response
from rest_framework.views import APIView
from seguridad.models.user_2 import User_2
from seguridad.models.seccion import Seccion
from rest_framework.authtoken.models import Token
from seguridad.services.menu import MenuService

class MenuApi(APIView):
    #regresa todas las opciones del menu agrupado por seccion
    def get(self,request,format = None):
        #token = request.GET.get("token")
        #usuario = Token.objects.get(key = token).user
        return Response(MenuService.getOpcionesMenu())
        #return Response("funciona")
