from django.db import models
from empenos.models.boleta_empeno import Boleta_Empeno
from django.contrib.auth.models import User

class Venta_Temporal_Piso(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT)

	class Meta:
		unique_together=("usuario","boleta")
