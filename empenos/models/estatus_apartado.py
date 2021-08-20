from django.db import models
class Estatus_Apartado(models.Model):
	estatus=models.CharField(max_length=20,null=False)

	def __str__(self):
		return self.estatus