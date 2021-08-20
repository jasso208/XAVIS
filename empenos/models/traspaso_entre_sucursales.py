from django.db import models
from empenos.models.otros_ingresos import Otros_Ingresos
from empenos.models.retiro_efectivo import Retiro_Efectivo
#tabla de traspasos
class Traspaso_Entre_Sucursales(models.Model):
	retiro = models.ForeignKey(Retiro_Efectivo,on_delete = models.PROTECT)
	ingreso = models.ForeignKey(Otros_Ingresos,on_delete = models.PROTECT)
	visto = models.BooleanField(default=True)#Cuando se hace un traspaso, le lleva la notificacion a la sucursal destino, para notificarle que ha recibido dineros

