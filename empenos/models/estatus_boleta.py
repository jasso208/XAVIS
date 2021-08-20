from django.db import models
class Estatus_Boleta(models.Model):
	estatus=models.CharField(max_length=20,null=False)
	nombre_corto=models.CharField(max_length=2,null=False)

	def __str__(self):
		return self.estatus+' '+self.nombre_corto