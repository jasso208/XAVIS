from django.db import models
from empenos.models.tipo_movimiento import Tipo_Movimiento
from django.utils import timezone
from django.contrib.auth.models import User
from seguridad.models.sucursal import Sucursal
class Cajas(models.Model):
	folio=models.CharField(max_length=7,null=True)
	tipo_movimiento=models.ForeignKey(Tipo_Movimiento,on_delete=models.PROTECT)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)
	fecha=models.DateTimeField(default=timezone.now)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	importe=models.IntegerField(default=0)
	caja=models.CharField(max_length=1,null=False)
	real_tarjeta=models.IntegerField(default=0)
	real_efectivo=models.IntegerField(default=0)
	teorico_tarjeta=models.IntegerField(default=0)
	teorico_efectivo=models.IntegerField(default=0)
	diferencia=models.IntegerField(default=0)
	fecha_cierre=models.DateTimeField(null=True)
	centavos_10=models.IntegerField(default=0)
	centavos_50=models.IntegerField(default=0)
	pesos_1=models.IntegerField(default=0)
	pesos_2=models.IntegerField(default=0)
	pesos_5=models.IntegerField(default=0)
	pesos_10=models.IntegerField(default=0)
	pesos_20=models.IntegerField(default=0)
	pesos_50=models.IntegerField(default=0)
	pesos_100=models.IntegerField(default=0)
	pesos_200=models.IntegerField(default=0)
	pesos_500=models.IntegerField(default=0)
	pesos_1000=models.IntegerField(default=0)
	token_cierre_caja=models.IntegerField(null=True)
	comentario=models.TextField(default='')
	user_cierra_caja=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user",blank = True,null=True)
	usuario_real_abre_caja = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True,related_name = "usuario_real_abre_caja")
	estatus_guardado=models.IntegerField(default=0)#cuando esta cero es que nunca se ha guardado informacion de cierre de caja, por lo tanto 
												   #no debemos mostrarle el boton de cierre de caja.
												   #cuando es 1, es que ya se ha guardado al menos una vez, y ya podemos mostrar el boton de cerrar caja


	def __str__(self):
		estatus="CERRADA"
		if self.fecha_cierre==None:
			estatus="Abierta"

		return str(self.fecha)+' '+estatus