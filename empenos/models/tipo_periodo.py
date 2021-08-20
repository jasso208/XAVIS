from django.db import models

class Tipo_Periodo(models.Model):
	tipo_periodo=models.CharField(max_length=20,null=False)

	def __str__(self):
		return self.tipo_periodo