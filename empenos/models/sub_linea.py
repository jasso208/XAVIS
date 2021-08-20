from django.db import models
from empenos.models.linea import Linea
class Sub_Linea(models.Model):
	linea=models.ForeignKey(Linea,on_delete=models.PROTECT)
	sub_linea=models.CharField(max_length=100,null=False)

	def __str__(self):
		return self.sub_linea

	class Meta:
		# sort by "fecha" in descending order unless
		# overridden in the query with order_by()
		ordering = ['sub_linea']
