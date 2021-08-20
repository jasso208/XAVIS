from empenos.models.apartado import Apartado
from django.db import models
from empenos.models.abono_apartado import Abono_Apartado
from django.contrib.auth.models import User

class Imprime_Apartado(models.Model):
	usuario=models.OneToOneField(User,on_delete=models.PROTECT,null=True,blank=True)
	apartado=models.ForeignKey(Apartado,on_delete=models.PROTECT)
	abono=models.OneToOneField(Abono_Apartado,on_delete=models.PROTECT,null=True,blank=True)

