
from seguridad.models import seccion
from seguridad.models.seccion import Seccion
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
		unique_together = ('usuario','opcion_menu')


	
	@property
	def idSeccion(self):
		return self.opcion_menu.seccion.id

	def getPermisos(usuario):
		respuesta = []
		opciones = []
		secciones = Seccion.objects.all()
		for s in secciones:
			permisos = Permisos_Usuario.objects.filter(opcion_menu__seccion = s,usuario = usuario)
			
			opciones = []
			for p in permisos:
				opciones.append({"id":p.opcion_menu.id,"opcion":p.opcion_menu.desc_item,"url_menu":p.opcion_menu.url_menu})
			if permisos.exists():
				respuesta.append({"id_seccion":s.id,"seccion":s.desc_seccion,"opciones":opciones})

		return respuesta

