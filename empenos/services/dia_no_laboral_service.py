
from django.utils import timezone
from django.contrib.auth.models import User
from empenos.models.dia_no_laboral import Dia_No_Laboral
import datetime
class DiaNoLaboralService():
    fecha = timezone.now()
    user = User()

    def setDiaNoLaboral(fecha,user):
        resp = {}
        try:
            dia = Dia_No_Laboral.objects.get(fecha = fecha)
            resp = {"estatus":"0","msj":"El día ingresado se agregado anteriormente."}
            return resp
        except:
            pass
        try:
            dnl = Dia_No_Laboral()
            dnl.fecha = fecha
            dnl.user_alta = user
            dnl.save()
            resp = {"estatus":"1"}
        except:
            resp = {"estatus":"0","msj":"Error al guardar el día no laboral."}

        return resp

    def delDiaNoLaboral(id_fecha):
        try:
            Dia_No_Laboral.objects.get(id = id_fecha).delete()
        except:
            return False

        return True

    def getDiasNoLaboralPorAnio(year):
        resp = {}
        print("entro")
        if type(4) != type(year):
            resp = {"estatus":"0","msj":"El año es incorrecto."}
            return resp

        fecha_inicial = datetime.datetime(year,1,1,0,0)
        fecha_final = datetime.datetime(year,12,31,23,59)

        resp = {"estatus":"1","data":Dia_No_Laboral.objects.filter(fecha__range = (fecha_inicial,fecha_final)).order_by("fecha").values("id","fecha")}
        

        return resp








