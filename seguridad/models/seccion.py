from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Almacenamos la seccion del sistema que deseamos administrar
#por ejemplo: En el menu Administracion esta la opcion, alta de sucursal, baja de sucursal, etc
#en el ejemplo la seccion sera Administracion
class Seccion(models.Model):	
	desc_seccion = models.CharField(max_length  = 50,null = False)

	def __str__(self):
		return str(self.id) + ' ' + self.desc_seccion

