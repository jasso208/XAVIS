from django.db import models
from empenos.models.tipo_movimiento import Tipo_Movimiento
from seguridad.models.sucursal import Sucursal
class Control_Folios(models.Model):
	folio=models.IntegerField(default=0)
	tipo_movimiento=models.ForeignKey(Tipo_Movimiento,on_delete=models.PROTECT)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)
	
	def __str__(self):
		return self.sucursal.sucursal+' '+self.tipo_movimiento.tipo_movimiento

	class Meta:
		unique_together=('tipo_movimiento','sucursal',)	
