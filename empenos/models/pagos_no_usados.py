from django.db import models
from empenos.models.tipo_pago import Tipo_Pago
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.abono import Abono

#cuando se aplica un refrendo, y este genera un desemepeño, los pagos que no se usaron se eliminan,
#pero en caso  de querer cancelar el abono, vamos a necesitar recuperarlos
#en esta tabla se almacenan para poder restaurarlos.
class Pagos_No_Usados(models.Model):
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
	abono = models.ForeignKey(Abono,on_delete = models.PROTECT,related_name = "abono_genero",null = True, blank = True )#nos indica el abono que lo genero
	abono_respaldo = models.ForeignKey(Abono,on_delete = models.PROTECT,related_name = "abono_respaldo",null = True,blank = True)#el abono que genero el respaldo
