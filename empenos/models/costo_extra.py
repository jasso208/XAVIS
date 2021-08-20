from django.db import models
class Costo_Extra(models.Model):
	descripcion=models.CharField(max_length=50,null=False)
	costo=models.IntegerField(default=0)