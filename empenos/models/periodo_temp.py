from django.db import models
from django.contrib.auth.models import User
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.tipo_periodo import Tipo_Periodo
from empenos.models.pagos import Pagos

#tabla usada para la simulacion de pagos mensual.
class Periodo_Temp(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	consecutivo=models.IntegerField(default=0)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT,null=False,blank=True)
	fecha_vencimiento=models.DateTimeField(null=False)
	importe=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	tipo_periodo=models.ForeignKey(Tipo_Periodo,on_delete=models.PROTECT,null=False)
	pago=models.ForeignKey(Pagos,on_delete=models.PROTECT,null=True,blank=True)
	fecha_pago=models.DateTimeField(null=True,blank=True)
	vencido=models.CharField(max_length=1,default='N')
	pagado=models.CharField(max_length=1,default='N',null=False)