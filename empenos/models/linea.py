from django.db import models
from empenos.models.tipo_producto import Tipo_Producto

class Linea(models.Model):
	tipo_producto=models.ForeignKey(Tipo_Producto,on_delete=models.PROTECT)
	linea=models.CharField(max_length=100,null=False)

	def __str__(self):
		return self.linea
	class Meta:
		# sort by "fecha" in descending order unless
		# overridden in the query with order_by()
		ordering = ['linea']
