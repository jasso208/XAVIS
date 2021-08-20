from django.db import models
from django.contrib.auth.models import User
#esta configuracion es por sucursal.
class Porcentaje_Comision_PG(models.Model):	
	porcentaje = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	usuario = models.ForeignKey(User,on_delete = models.PROTECT,null=True,blank=True) #el usuario que actualiza por ultimavez
