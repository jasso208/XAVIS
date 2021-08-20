from django.db import models
from empenos.models.venta_granel import Venta_Granel
from empenos.models.boleta_empeno import Boleta_Empeno

class Det_Venta_Granel(models.Model):
	venta=models.ForeignKey(Venta_Granel,on_delete=models.PROTECT)
	boleta=models.OneToOneField(Boleta_Empeno,on_delete=models.PROTECT)