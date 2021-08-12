from django.db.models.deletion import PROTECT
from seguridad.models.perfil import Perfil
from django.db import models
from seguridad.models.menu import Menu

class PermisosPerfil(models.Model):
    perfil = models.ForeignKey(Perfil,on_delete=models.PROTECT)
    opcion = models.ForeignKey(Menu,on_delete= models.PROTECT)

    class Meta:
        unique_together = ("perfil","opcion")