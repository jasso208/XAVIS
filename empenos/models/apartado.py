from django.db import models
from empenos.models.cliente import Cliente
from empenos.models.estatus_apartado import Estatus_Apartado
from empenos.models.boleta_empeno import Boleta_Empeno
from seguridad.models.sucursal import Sucursal
from django.utils import timezone
from django.contrib.auth.models import User
from empenos.models.cajas import Cajas

class Apartado(models.Model):
	folio=models.CharField(max_length=7,null=True)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name="usuario_apartado")#el usuario que realiza la venta en el sistema
	fecha=models.DateTimeField(default=timezone.now)		
	importe_venta=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)#es elimporte real de la venta, en cuanto realmente se vendio el producto
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)#es la caja que se tenia aberta cuando se ingreso el dinero.
	cliente=models.ForeignKey(Cliente,on_delete=models.PROTECT,blank=True,null=True)
	saldo_restante=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)#es el importe que falta para terminar de pagar la prenda.
	estatus=models.ForeignKey(Estatus_Apartado,on_delete=models.PROTECT,null=True,blank=True)
	boleta=models.OneToOneField(Boleta_Empeno,on_delete=models.PROTECT,null=True,blank=True)#como solo una boleta puede estar apartada a la vez, no necesitamos el detalle.
	fecha_vencimiento=models.DateTimeField(null=True,blank=True)
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT,blank=True,null=True)	
	nombre_cliente = models.CharField(max_length = 100,default = '')
	telefono = models.CharField(max_length = 10,default = '')
