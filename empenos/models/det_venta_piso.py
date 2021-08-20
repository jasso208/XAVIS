from django.db import models
from empenos.models.venta_piso import Venta_Piso
from empenos.models.boleta_empeno import Boleta_Empeno

class Det_Venta_Piso(models.Model):
	venta=models.ForeignKey(Venta_Piso,on_delete=models.PROTECT)
	boleta=models.OneToOneField(Boleta_Empeno,on_delete=models.PROTECT)
	importe_venta=models.IntegerField(default=0)