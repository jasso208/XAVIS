import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from seguridad.models.sucursal import Sucursal
from empenos.models.tipo_producto import Tipo_Producto
class InteresEmpeno(models.Model):
    sucursal = models.ForeignKey(Sucursal,on_delete = models.PROTECT,null = False)
    tipo_prodcto = models.ForeignKey(Tipo_Producto,on_delete = models.PROTECT,null = False)
    almacenaje = models.FloatField()
    iva = models.FloatField()
    interes = models.FloatField()
    usuario_alta = models.ForeignKey(User,on_delete = models.PROTECT,related_name="usuario_alta")
    fecha_alta = models.DateTimeField(default = timezone.now())
    usuario_modifica = models.ForeignKey(User,on_delete = models.PROTECT,related_name="usuario_modifica")
    fecha_modifica = models.DateTimeField(default = timezone.now())
