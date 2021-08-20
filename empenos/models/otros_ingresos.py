from django.db import models
from empenos.models.tipo_movimiento import Tipo_Movimiento
from seguridad.models.sucursal import Sucursal
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from empenos.models.cajas import Cajas
SI_NO=(
	('1','SI'),
	('2','NO'),
)

class Otros_Ingresos(models.Model):
	folio = models.CharField(max_length=7,null=True)
	tipo_movimiento = models.ForeignKey(Tipo_Movimiento,on_delete=models.PROTECT)
	sucursal = models.ForeignKey(Sucursal,on_delete=models.PROTECT)
	fecha = models.DateTimeField(default=timezone.now)
	usuario = models.ForeignKey(User,on_delete=models.PROTECT) #
	importe = models.IntegerField(default=0, validators=[MinValueValidator(Decimal('1'))])
	comentario = models.CharField(max_length=200,default='')
	caja = models.CharField(max_length=1,null=True)
	activo = models.CharField(choices = SI_NO,default = 1, max_length=2)
	ocaja = models.ForeignKey(Cajas,on_delete = models.PROTECT,null = True,blank = True)
