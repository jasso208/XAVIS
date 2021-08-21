from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from empenos.services.dia_no_laboral_service import DiaNoLaboralService
class DiaNoLaboralApi(APIView):

    def get(self,request,format = None):
        
        try:
            year = int(request.GET.get("year"))
        except:
            return Response({"estatus":"0","msj":"El año es incorrecto."})
        return Response(DiaNoLaboralService.getDiasNoLaboralPorAnio(year))

    def post(self,request,format = None):
        fecha = request.data["fecha"]
        token = request.data["token"]

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({"estatus":"0","msj":"Debe iniciar session para realizar esta accion."})

        return Response(DiaNoLaboralService.setDiaNoLaboral(fecha,user))

    def delete(self,request,id_fecha,format = None):
        print(id_fecha)
   
        return Response(DiaNoLaboralService.delDiaNoLaboral(id_fecha))