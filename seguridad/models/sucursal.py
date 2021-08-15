from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, time,timedelta
from django.db.models import Sum,Max

import decimal
class Sucursal(models.Model):
	sucursal=models.CharField(max_length=100,null=False)
	calle=models.CharField(max_length=50,null=True,default='')
	codigo_postal=models.CharField(max_length=10,null=True,default='')
	numero_interior=models.IntegerField(default=0,null=True)
	numero_exterior=models.IntegerField(default=0,null=True)
	colonia=models.CharField(max_length=50,null=True,default='')
	ciudad=models.CharField(max_length=50,null=True,default='')
	estado=models.CharField(max_length=50,null=True,default='')
	pais=models.CharField(max_length=50,null=True,default='')
	telefono=models.CharField(max_length=10,null=True,default='')
	saldo = models.IntegerField(default=0)
	usuario_virtual = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True)

	def __str__(self):
		return self.sucursal
		
"""
	def fn_abre_caja(self,importe_apertura,usuario_apertura):
		hoy = date.today()

		hoy_min = datetime.combine(hoy,time.min)
		hoy_max = datetime.combine(hoy,time.max)

		resp = []

		#validamos que la sucursal no tenga caja abierta		
		caja = Cajas.objects.filter(fecha_cierre__isnull = True,sucursal = self)
		if caja.exists():
			resp.append(False)			
			resp.append("La sucursal cuenta con caja abierta. Solo puede abrir una caja por sucursal.")
			return resp

		#buscamos el importe con el que cerro la ultima caja
		ultima_caja = Cajas.objects.filter(sucursal = self).aggregate(Max("id"))["id__max"]
		importe_ultima_caja = 0#si es la primera vez que se apertura caja el importe es cero, de lo contrario, se toma el importe con el que cerro anteriormente
		if ultima_caja != None: 
			importe_ultima_caja = Cajas.objects.get(id = int(ultima_caja)).teorico_efectivo

		if float(importe_apertura) != float(importe_ultima_caja) or float(importe_apertura) != self.saldo:
			resp.append(False)			
			resp.append("El importe con el que desea aperturar, es diferente al importe con el que cerro la ùltima caja.")
			return resp

		if self.usuario_virtual == None:
			resp.append(False)			
			resp.append("La sucursal no tiene asignado usuario virtual, contacte con el administrador del sistema.")
			return resp

		caja_abierta = Cajas.objects.filter(fecha__range = (hoy_min,hoy_max),sucursal = self,fecha_cierre__isnull = False)

		if caja_abierta.exists():
			resp.append(False)			
			resp.append("La caja de esta sucursal ya fue cerrada.")
			return resp

		tm = Tipo_Movimiento.objects.get(id=1)
		folio = fn_folios(tm,self)
		str_folio = fn_str_clave(folio)

		caja = Cajas()
		
		caja.folio = str_folio
		caja.tipo_movimiento = tm
		caja.sucursal = self		
		caja.usuario = self.usuario_virtual
		caja.importe = float(importe_apertura)
		caja.caja = "A"#como solo se puede aperturar una caja por sucursal, siempre sera la caja A
		caja.usuario_real_abre_caja = usuario_apertura
		caja.save()

		resp.append(True)	

		return resp
		
	#si no contamos con caja abierta, regresa None
	def fn_get_caja_abierta(self):
		hoy = date.today()
		hoy_min = datetime.combine(hoy,time.min)
		hoy_max = datetime.combine(hoy,time.max)

		try:
			#buscamos la caja abierta
			caja = Cajas.objects.get(fecha__range = (hoy_min,hoy_max),sucursal = self,fecha_cierre__isnull = True)
		except:
			caja = None

		return caja





    def fn_actualiza_porcentaje_mutuo(self,porcentaje_oro,porcentaje_plata,porcentaje_articulos_varios):

		#validamos que los valores sean enteros
		if type(porcentaje_oro) != type(0):
			return False

		if type(porcentaje_plata) != type(0):
			return False

		if type(porcentaje_articulos_varios) != type(0):
			return False

		if porcentaje_oro <= 0:
			return False

		if porcentaje_plata <= 0:
			return False

		if porcentaje_articulos_varios <= 0:
			return False			

		try:
			cpm = Configuracion_Porcentaje_Mutuo.objects.get(sucursal = self)
		except Exception as e:#si falla es porque aun no tiene configurada el porcentaje mutuo
			
			cpm = Configuracion_Porcentaje_Mutuo()
			cpm.sucursal = self

		cpm.porcentaje_oro = porcentaje_oro
		cpm.porcentaje_plata = porcentaje_plata
		cpm.porcentaje_articulos_varios = porcentaje_articulos_varios
		cpm.save()

		return True

	def fn_consulta_porcentaje_mutuo(self):
		try:
			return Configuracion_Porcentaje_Mutuo.objects.get(sucursal = self)
		except Exception as e:			
			return False

	#recibe el tipo de producto y regresa el interes que le corresponde a ese tipo de producto
	def fn_get_interes(self,tipo_producto):

		cpm = Configuracion_Interes_Empeno.objects.get(sucursal = self)

		#si es oro
		if tipo_producto == 1:
			return cpm.interes_oro
		elif tipo_producto == 2:
			return cpm.interes_plata
		elif tipo_producto == 3:
			return cpm.interes_prod_varios
		else:
			return 0


	#recibe como parametro el tipo de producto y regresa el porcentaje de almacenje que le corresponde a ese tipo de producto
	def fn_get_almacenaje(self,tipo_producto):
		cpm = Configuracion_Interes_Empeno.objects.get(sucursal = self)

		#si es oro
		if tipo_producto == 1:
			return cpm.almacenaje_oro
		elif tipo_producto == 2:
			return cpm.almacenaje_plata
		elif tipo_producto == 3:
			return cpm.almacenaje_prod_varios
		else:
			return 0

	#recibe como parametro el tipo de producto y regresa el porcentaje de IVA que le corresponde a ese tipo de producto
	def fn_get_iva(self,tipo_producto):
		cpm = Configuracion_Interes_Empeno.objects.get(sucursal = self)

		#si es oro
		if tipo_producto == 1:
			return cpm.iva_oro
		elif tipo_producto == 2:
			return cpm.iva_plata
		elif tipo_producto == 3:
			return cpm.iva_prod_varios
		else:
			return 0

	#funcion que recibe el mutuo y el tipo de producto para calcular el refrendo que le corresponde
	# considerando la sucursal en la que se encuentra. y la configuracion de la tabla Configuracion_Interes_Empeno
	# este se usa solo para la cotizacion, ya que para guardar el refrendo en la boleta se usa la funcion de el modelo Boleta Empeno
	def fn_calcula_refrendo(self,mutuo,tipo_producto):
		
		almacenaje = 0.00
		interes = 0.00
		iva=0.00
		refrendo = 0.00
		respuesta = []

		try:
			cie = Configuracion_Interes_Empeno.objects.get(sucursal = self)
		except:
			#el estatus cero es error al encontrar la configuracion de interes empeno
			respuesta.append({"estatus":"0","almacenaje":0,"interes":0,"iva":0,"refrendo":0})
			return respuesta

		if tipo_producto == 1 :#Oro

			p_almacenaje = cie.almacenaje_oro/100
			p_interes = cie.interes_oro/100
			p_iva  = cie.iva_oro/100

		elif tipo_producto == 2:#plata
			p_almacenaje = cie.almacenaje_plata/100
			p_interes = cie.interes_plata/100
			p_iva  = cie.iva_plata/100

		else:		

			p_almacenaje = cie.almacenaje_prod_varios /100
			p_interes = cie.interes_prod_varios /100
			p_iva  = cie.iva_prod_varios /100

		almacenaje = (mutuo * p_almacenaje)
		interes = (mutuo * p_interes)
		iva = ((almacenaje+interes) * p_iva)
		refrendo = round(almacenaje+interes+iva)
		respuesta.append({"estatus":"1","almacenaje":almacenaje,"interes":interes,"iva":iva,"refrendo":refrendo})
		
		return respuesta


	#funcion que recibe un rango de fechas y regresa el importe total de refrendos recibidos	
	def fn_get_total_refrendos(self,fecha_i,fecha_f):
		abonos = Abono.objects.filter(fecha__range = (fecha_i,fecha_f),sucursal = self)
		refrendo  = 0.00
		for a in abonos:
			#Buscamos los refrendos  de las boletas de plazo semanal.
			rap = Rel_Abono_Pago.objects.filter(abono = a)
			for r in rap:
				
				#si afecto a un refrendo o refrendo pg, lo contamos como refrendo				
				if r.pago.tipo_pago.id == 1 or r.pago.tipo_pago.id == 3:

					refrendo = decimal.Decimal(refrendo) + decimal.Decimal(r.pago.importe)

			#buscamos las boletas de plazo mensual
			rap = Rel_Abono_Periodo.objects.filter(abono = a)
			for r in rap:
				refrendo = decimal.Decimal(refrendo) + decimal.Decimal(r.periodo.importe)				

		return refrendo

	#funcion que recibe un rango de fecas y regresa el importe total de pagos a comision pg
	def fn_get_total_comision_pg(self,fecha_i,fecha_f):
		abonos = Abono.objects.filter(fecha__range = (fecha_i,fecha_f),sucursal = self)
		comision_pg  = 0.00
		for a in abonos:			
			rap = Rel_Abono_Pago.objects.filter(abono = a)
			for r in rap:				
				#Solo contamos los tipos de pagos comision pg
				if r.pago.tipo_pago.id == 2:
					comision_pg = decimal.Decimal(comision_pg) + decimal.Decimal(r.pago.importe)

		return comision_pg

	#funcion que recibe un rango de fechas y regresa el importe de costos extras.
	#al momento de crear esta rutina, solo existe el cobro reimpresion de boleta.
	def fn_get_total_costos_extras(self,fecha_i,fecha_f):
		rce = Reg_Costos_Extra.objects.filter(fecha__range = (fecha_i,fecha_f),caja__sucursal = self).aggregate(Sum("importe"))

		total_costo_extra = 0

		if rce["importe__sum"] != None:
			total_costo_extra = rce["importe__sum"]

		return decimal.Decimal(total_costo_extra)

	#funcin que recibe un rango de fechas y regresa la ganancia de las ventas.
	#importe_venta - mutuo_real = ganancia el ventas.
	def fn_get_ganancia_ventas(self,fecha_i,fecha_f):
		importe_mutuo = 0
		importe_venta = 0

		im = Venta_Piso.objects.filter(sucursal = self, fecha__range = (fecha_i,fecha_f)).aggregate(Sum("importe_mutuo"))
		if im["importe_mutuo__sum"]!= None:
			importe_mutuo = im["importe_mutuo__sum"]

		img = Venta_Granel.objects.filter(sucursal = self, fecha__range = (fecha_i,fecha_f)).aggregate(Sum("importe_mutuo"))
		if img["importe_mutuo__sum"]!= None:
			importe_mutuo = decimal.Decimal(importe_mutuo)+ decimal.Decimal(img["importe_mutuo__sum"])



		iv = Venta_Piso.objects.filter(sucursal = self, fecha__range = (fecha_i,fecha_f)).aggregate(Sum("importe_venta"))
		if iv["importe_venta__sum"]!= None:
			importe_venta = iv["importe_venta__sum"]	


		ivg = Venta_Granel.objects.filter(sucursal = self, fecha__range = (fecha_i,fecha_f)).aggregate(Sum("importe_venta"))
		if ivg["importe_venta__sum"]!= None:
			importe_venta = decimal.Decimal(importe_venta) + decimal.Decimal(ivg["importe_venta__sum"])

		return decimal.Decimal(importe_venta) - decimal.Decimal(importe_mutuo)

	def fn_get_retiros(self,fecha_i,fecha_f):

		ret=Retiro_Efectivo.objects.filter(sucursal=self,fecha__range=(fecha_i,fecha_f),activo = 1).aggregate(Sum("importe"))

		importe_retiros=0.00					
		if ret["importe__sum"]!=None:
			importe_retiros=ret["importe__sum"]

		return importe_retiros			
"""