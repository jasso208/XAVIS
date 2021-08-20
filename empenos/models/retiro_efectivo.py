from django.db import models
from empenos.models.tipo_movimiento import Tipo_Movimiento
from seguridad.models.sucursal import Sucursal
from empenos.models.concepto_retiro import Concepto_Retiro
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from empenos.models.cajas import Cajas
SI_NO=(
	('1','SI'),
	('2','NO'),
)

class Retiro_Efectivo(models.Model):
	folio=models.CharField(max_length = 7,null = True)
	tipo_movimiento=models.ForeignKey(Tipo_Movimiento,on_delete = models.PROTECT)
	sucursal=models.ForeignKey(Sucursal,on_delete = models.PROTECT)
	fecha=models.DateTimeField(default = timezone.now)
	usuario=models.ForeignKey(User,on_delete = models.PROTECT,related_name = "usuario_alta")
	importe=models.IntegerField(default = 0, validators = [MinValueValidator(Decimal('1'))])
	comentario=models.TextField(default = '',max_length = 100)
	caja=models.CharField(max_length = 1,null = True)
	token=models.IntegerField()
	concepto = models.ForeignKey(Concepto_Retiro,on_delete = models.PROTECT,blank = True,null = True)
	#no requerimos fecha de cancelacion ya que solo se puede cancelar el dia en que se genera.
	usuario_cancela = models.ForeignKey(User,on_delete = models.PROTECT,null = True, blank = True,related_name = 'usuario_cancela')
	activo = models.CharField(choices = SI_NO,default = 1, max_length=2)
	ocaja = models.ForeignKey(Cajas,on_delete = models.PROTECT,null = True,blank = True)

	def fn_cancela_retiro(self,id_usuario_cancela,comentario_cancelacion):
		try:
			self.importe = 0
			self.comentario = comentario_cancelacion
			self.usuario_cancela = User.objects.get(id = int(id_usuario_cancela))
			self.activo = 2# no activo
			self.save()
			return True
		except:
			return False
