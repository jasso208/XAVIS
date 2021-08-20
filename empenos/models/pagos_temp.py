from django.db import models
from empenos.models.tipo_pago import Tipo_Pago
from django.contrib.auth.models import User
from empenos.models.boleta_empeno import Boleta_Empeno

#tabla usada para la simulacion tipo_pago import Tipo_Pago
# from django.contrib.auth.models import User
# from empenos.models.boleta_empeno importe pagos semanal
class Pagos_Temp(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	tipo_pago=models.ForeignKey(Tipo_Pago,on_delete=models.PROTECT,null=False,blank=True)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT,null=False,blank=True)
	fecha_vencimiento=models.DateTimeField(null=False)
	almacenaje=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	interes=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	iva=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	importe=models.IntegerField()
	vencido=models.CharField(max_length=1,default='N')
	pagado=models.CharField(max_length=1,default='N',null=False)
	fecha_pago=models.DateTimeField(null=True,blank=True)
	fecha_vencimiento_real=models.DateTimeField(null=True,blank=True)
