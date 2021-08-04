from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seguridad.models.seccion import Seccion

class Menu(models.Model):
	desc_item = models.CharField(max_length = 50,null = False)
	vista = models.CharField(max_length = 50,null = False) #la vista a la que hace referencia
	app = models.CharField(max_length = 50,null = False)#la appa  ala que pertenece la vista.
	seccion = models.ForeignKey(Seccion,on_delete = models.PROTECT,null = False,blank = False) #la seccion a la que pertenece la vista.

	def __str__(self):
		return str(self.id) + ' ' + self.desc_item