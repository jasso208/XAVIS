from django.db import models
from empenos.models.tipo_producto import Tipo_Producto
from empenos.models.tipo_kilataje import Tipo_Kilataje
from django.db import transaction
class Kilataje(models.Model):	
	tipo_producto = models.ForeignKey(Tipo_Producto,on_delete=models.PROTECT,blank=True,null=False)
	kilataje = models.CharField(max_length=10,null=False)
	avaluo = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	tipo_kilataje = models.ForeignKey(Tipo_Kilataje,on_delete=models.PROTECT,default = 2)
	activo = models.CharField(max_length=1,default="S")
	
	def __str__(self):
		return self.tipo_producto.tipo_producto+' '+self.kilataje+' $'+str(self.avaluo)

	#con la finalidad de poder saber cual el importe que tenia el kilataje
	#al momento de haer un empeño, no se edita, mas bien se desactiva el primero
	# y se crea uno nuevo con el nuevo importe.
	@transaction.atomic
	def fn_actualiza_kilataje(self,nuevo_importe):
		try:
			#creamos un kilataje igual pero con diferente precio
			Kilataje.objects.create(tipo_producto=self.tipo_producto,kilataje=self.kilataje,avaluo=nuevo_importe,tipo_kilataje=self.tipo_kilataje)
			#desactivamos el actual kilataje
			self.activo="N"
			self.save()
			return True
		except:
			transaction.set_rollback(True)
			return False
