from django.db import models
class Marca(models.Model):	
	marca=models.CharField(max_length=100,null=False)

	def __str__(self):
		return self.marca
	class Meta:
		# sort by "fecha" in descending order unless
		# overridden in the query with order_by()
		ordering = ['marca']