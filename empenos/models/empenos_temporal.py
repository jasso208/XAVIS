from django.db import models
from empenos.models.tipo_producto import Tipo_Producto
from empenos.models.sub_linea import Sub_Linea
from empenos.models.linea import Linea
from empenos.models.marca import Marca
from django.contrib.auth.models import User
from django.db.models import Sum,Max

class Empenos_Temporal(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	tipo_producto=models.ForeignKey(Tipo_Producto,on_delete=models.PROTECT)
	linea=models.ForeignKey(Linea,on_delete=models.PROTECT)
	sub_linea=models.ForeignKey(Sub_Linea,on_delete=models.PROTECT)	
	marca=models.ForeignKey(Marca,on_delete=models.PROTECT)
	descripcion=models.CharField(max_length=50,null=False)
	avaluo=models.IntegerField()
	mutuo_sugerido=models.IntegerField()
	mutuo=models.IntegerField()
	observaciones=models.TextField(null=True,blank=True)

	def get_mutuo_temporal(usuario):
		et_oro = Empenos_Temporal.objects.filter(usuario = usuario,tipo_producto__id = 1)		
		et_plata = Empenos_Temporal.objects.filter(usuario = usuario,tipo_producto__id = 2)		
		et_varios = Empenos_Temporal.objects.filter(usuario = usuario,tipo_producto__id = 3)		

		lista = []
		mutuo_oro = 0.00
		if et_oro.exists():
			mutuo_oro = et_oro.aggregate(Sum("mutuo"))["mutuo__sum"]

		mutuo_plata = 0.00
		if et_plata.exists():
			mutuo_plata = et_plata.aggregate(Sum("mutuo"))["mutuo__sum"]

		mutuo_varios = 0.00
		if et_varios.exists():
			mutuo_varios = et_varios.aggregate(Sum("mutuo"))["mutuo__sum"]


		lista.append({"mutuo_oro":mutuo_oro,"mutuo_plata":mutuo_plata,"mutuo_varios":mutuo_varios})

		return lista

