from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seguridad.models.seccion import Seccion
class Menu(models.Model):
	desc_item = models.CharField(max_length = 50,null = False)
	url_menu = models.CharField(max_length= 100,null = False,default = "na")#url a que direcciona la opcion
	seccion = models.ForeignKey(Seccion,on_delete = models.PROTECT,null = False,blank = False) #la seccion a la que pertenece la vista.
	orden = models.IntegerField(default = 1)#indica el orden en que se mostrara dentro del menu, entre menor sea el numero, mas arriba aparecera.
	comentario = models.CharField(max_length=1000,null=True)
	visible = models.IntegerField(default=1100)#indica si es visible en el menu lateral del front, 1: si es visible: 0 no es viisble.
	
	def __str__(self):
		return str(self.id) + ' ' + self.desc_item


	

