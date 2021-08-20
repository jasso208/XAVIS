
from django.db import models 
from django.contrib.auth.models import User

class Min_Apartado(models.Model):
	porc_min_1_mes=models.IntegerField()
	porc_min_2_mes=models.IntegerField()
	a_criterio_cajero = models.BooleanField( default = False);
	usuario_modifica = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True)
