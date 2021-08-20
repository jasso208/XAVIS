from django.db import models
class Tipo_Movimiento(models.Model):
	tipo_movimiento=models.CharField(max_length=50,null=False)
	naturaleza=models.CharField(max_length=20,null=False)

	def __str__(self):
		return self.tipo_movimiento