
from django.db import models
from seguridad.models.sucursal import Sucursal

class Configuracion_Porcentaje_Mutuo(models.Model):
	sucursal = models.OneToOneField(Sucursal,on_delete=models.PROTECT)
	porcentaje_oro = models.IntegerField()
	porcentaje_plata = models.IntegerField()
	porcentaje_articulos_varios = models.IntegerField()

