from django.db import models
class Tipo_Pago(models.Model):
	tipo_pago=models.CharField(max_length=30,null=False)

	def __str__(self):
		return self.tipo_pago