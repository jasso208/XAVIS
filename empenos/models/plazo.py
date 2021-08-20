from django.db import models
class Plazo(models.Model):
	plazo=models.CharField(max_length=30,null=False)

	def __str__(self):
		return self.plazo