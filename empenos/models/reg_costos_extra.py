from empenos.models.costo_extra import Costo_Extra
from django.db import models
from empenos.models.cajas import Cajas
from django.utils import timezone
from empenos.models.boleta_empeno import Boleta_Empeno

class Reg_Costos_Extra(models.Model):
	costo_extra=models.ForeignKey(Costo_Extra,on_delete=models.PROTECT)
	fecha=models.DateTimeField(default=timezone.now)
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT)
	importe=models.IntegerField()
