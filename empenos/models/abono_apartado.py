from django.db import models
from empenos.models.cajas import Cajas
from empenos.models.apartado import Apartado
from django.utils import timezone
from django.contrib.auth.models import User

class Abono_Apartado(models.Model):
	folio=models.CharField(max_length=7,null=True)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name="usuario_ab_apartado")
	fecha=models.DateTimeField(default=timezone.now)		
	importe=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)#es la caja que se tenia aberta cuando se ingreso el dinero.
	apartado=models.ForeignKey(Apartado,on_delete=models.PROTECT)
