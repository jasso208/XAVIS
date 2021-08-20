from django.db import models
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.tipo_pago import Tipo_Pago
from empenos.models.abono import Abono

class Pagos(models.Model):
	tipo_pago=models.ForeignKey(Tipo_Pago,on_delete=models.PROTECT,null=False,blank=True)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT,null=False,blank=True)
	fecha_vencimiento=models.DateTimeField(null=False)
	almacenaje=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	interes=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	iva=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	importe=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	vencido=models.CharField(max_length=1,default='N')
	pagado=models.CharField(max_length=1,default='N',null=False)
	fecha_pago=models.DateTimeField(null=True,blank=True)
	fecha_vencimiento_real=models.DateTimeField(null=True,blank=True)#cuando la fecha de vencimiento cai en dia de asueto, la fecha de vencimienot se recorre un dia, esta fecha nos indica cual es la fecha de vencimiento real para calcular el las futuras fechas de vencimiento.
	abono = models.ForeignKey(Abono,on_delete = models.PROTECT,null = True,blank = True)#Nos indica cual abono lo genero, para en caso de cancelar el abono, debemos eliminar el pago.


