from django.db import models
from empenos.models.venta_piso import Venta_Piso
from django.contrib.auth.models import User

class Imprime_Venta_Piso(models.Model):
	usuario=models.OneToOneField(User,on_delete=models.PROTECT,null=True,blank=True)
	venta_piso=models.ForeignKey(Venta_Piso,on_delete=models.PROTECT)