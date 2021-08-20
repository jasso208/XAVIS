from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seguridad.models.sucursal import Sucursal
from empenos.models.cajas import Cajas

class Venta_Granel(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name="usuario2")#el usuario que realiza la venta en el sistema
	fecha=models.DateTimeField(default=timezone.now)	
	importe_mutuo=models.DecimalField(max_digits=20,decimal_places=2)
	importe_avaluo=models.DecimalField(max_digits=20,decimal_places=2)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)	
	importe_venta=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)#es elimporte real de la venta, en cuanto realmente se vendio el granel
	usuario_finaliza=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name="usuario_finaliza")#el usuario que fisicamente realiza la venta y da ingreso al dinero de la venta		
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)#es la caja que se tenia aberta cuando se ingreso el dinero.
	fecha_importe_venta=models.DateTimeField(null=True,blank=True)
