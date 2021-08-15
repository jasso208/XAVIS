from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.models.sucursal import Sucursal
class SucursalApi(APIView):

    def get(self,request,format = None):
        
        sucursales = Sucursal.objects.all().values("id","sucursal")

        return Response(sucursales)



