from django.db import models
from django.contrib.auth.models import User
from empenos.models.venta_granel import Venta_Granel

class Imprime_Venta_Granel(models.Model):
	usuario=models.OneToOneField(User,on_delete=models.PROTECT,null=True,blank=True)
	venta_granel=models.ForeignKey(Venta_Granel,on_delete=models.PROTECT)
