from rest_framework.response import Response
from  rest_framework.views import APIView
from empenos.services.kilataje_service import KilatajeService
class KilatajeApi(APIView):

    def get(self,request,format = None):
        return Response(KilatajeService.getAllKilatajes())
    
    def post(self,request,format = None):
        id_tipo_producto = request.data["tipo_producto"]
        id_tipo_kilataje =  request.data["tipo_kilataje"]
        kilataje = request.data["kilataje"]
        avaluo = request.data["avaluo"]
        return Response(KilatajeService.addKilataje(id_tipo_producto,id_tipo_kilataje,kilataje,avaluo))

    def put(self,request,format = None):
        id = int(request.data["id"])
        return Response(KilatajeService.desactivaKilataje(id))
