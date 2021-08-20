from django.db import models
from seguridad.models.sucursal import Sucursal
from empenos.models.cajas import Cajas
from empenos.models.cliente import Cliente
from django.utils import timezone
from django.contrib.auth.models import User

class Venta_Piso(models.Model):
	folio=models.CharField(max_length=7,null=True)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name="usuario")#el usuario que realiza la venta en el sistema
	fecha=models.DateTimeField(default=timezone.now)	
	importe_mutuo=models.DecimalField(max_digits=20,decimal_places=2)
	importe_avaluo=models.DecimalField(max_digits=20,decimal_places=2)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)	
	importe_venta=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)#es elimporte real de la venta, en cuanto realmente se vendio el granel
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)#es la caja que se tenia aberta cuando se ingreso el dinero.
	cliente=models.ForeignKey(Cliente,on_delete=models.PROTECT,blank=True,null=True)
	nombre_cliente = models.CharField(max_length = 100,default = '')
	telefono = models.CharField(max_length = 10,default = '')
