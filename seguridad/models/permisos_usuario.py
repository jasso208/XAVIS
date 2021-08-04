from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seguridad.models.menu import Menu

# almacenamos a que vistas tiene acceso el usuario
class Permisos_Usuario(models.Model):
	usuario = models.ForeignKey(User,on_delete = models.PROTECT,related_name = "usuario_permiso")
	opcion_menu = models.ForeignKey(Menu,on_delete = models.PROTECT)
	usuario_otorga = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True,related_name = "usuario_otorga")

	class Meta:
		unique_together = ('usuario','opcion_menu',) 