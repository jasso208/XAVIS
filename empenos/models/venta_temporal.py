from django.db import models
from empenos.models.boleta_empeno import Boleta_Empeno
from django.contrib.auth.models import User

class Venta_Temporal(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT,null=True,blank=True)
	fecha=models.DateTimeField(null=True,blank=True)#la venta temporal se almacena por un dia, al siguiente dia se elimina.q
	vender=models.CharField(max_length=1,default='N')

	class Meta:
		unique_together=("usuario","boleta")