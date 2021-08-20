from django.db import models
from empenos.models.abono import Abono
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.tipo_pago import Tipo_Pago

#cuando se aplica un refrendo y se le descuento los periodos PG
#se almacenan en esta tabla durante el dia, esto con la finalidad de poder cancelar
#el refrendo en caso de querer. asi podemos regresar los abonos pg.
# por la noche deberan borrarse.
class Pagos_Com_Pg_No_Usados(models.Model):
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
	abono = models.ForeignKey(Abono,on_delete = models.PROTECT)
