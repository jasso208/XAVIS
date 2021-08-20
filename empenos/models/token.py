from django.db import models
from seguridad.models.sucursal import Sucursal
from empenos.models.tipo_movimiento import Tipo_Movimiento
from django.contrib.auth.models import User
from django.utils import timezone

class Token(models.Model):
	tipo_movimiento=models.ForeignKey(Tipo_Movimiento,on_delete=models.PROTECT)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)
	caja=models.CharField(max_length=1,null=True)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	token=models.IntegerField()
	fecha=models.DateTimeField(default=timezone.now)
	aux_1 = models.IntegerField(null = True,blank = True)