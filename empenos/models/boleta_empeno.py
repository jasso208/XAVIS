from django.db import models
from empenos.models.tipo_producto import Tipo_Producto
from django.utils import timezone
from django.contrib.auth.models import User
from empenos.models.cliente import Cliente
from empenos.models.plazo import Plazo
from empenos.models.estatus_boleta import Estatus_Boleta
from empenos.models.cajas import Cajas
from seguridad.models.sucursal import Sucursal

from django.db.models import Sum,Max,Min
class Boleta_Empeno(models.Model):
	folio=models.IntegerField(null=False)
	tipo_producto=models.ForeignKey(Tipo_Producto,on_delete=models.PROTECT)
	caja=models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,related_name = "usuario_empena")
	avaluo=models.IntegerField()
	mutuo=models.IntegerField()	#este campo se ira actualizando cuando se abona a capital
	fecha=models.DateTimeField(default=timezone.now)
	fecha_vencimiento=models.DateTimeField()
	cliente=models.ForeignKey(Cliente,on_delete=models.PROTECT)
	nombre_cotitular=models.CharField(max_length=20,default='NA')
	apellido_p_cotitular=models.CharField(max_length=20,default='NA')
	apellido_m_cotitular=models.CharField(max_length=20,default='NA')
	plazo=models.ForeignKey(Plazo,on_delete=models.PROTECT)
	refrendo=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	estatus=models.ForeignKey(Estatus_Boleta,on_delete=models.PROTECT,default=1,related_name = "estatus_b")
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT,blank=True,null=True)
	mutuo_original=models.IntegerField(default=0)	#este campo no se actualiza, nos sirve para saber cual fue el mutuo original de la boleta.
	fecha_vencimiento_real=models.DateTimeField(null=True,blank=True)#cuando la fecha de vencimiento cai en dia de asueto, la fecha de vencimienot se recorre un dia, esta fecha nos indica cual es la fecha de vencimiento real para calcular el las futuras fechas de vencimiento.
	almacenaje = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0)
	interes = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0)
	iva = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0)
	fecha_vencimiento_anterior = models.DateTimeField(null = True, blank = True)
	estatus_anterior = models.ForeignKey(Estatus_Boleta,on_delete = models.PROTECT, related_name = "estatus_anterior",null = True,blank = True)
	fecha_vencimiento_real_anterior = models.DateTimeField(null = True, blank = True)
	precio_venta_fijo = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0 ) #Cuando el precio de venta que se calcula en base a la configuracion de la tabla Porcentaje_Sobre_Avaluo
	#																					     no es el correcto, se establece un precio fijo.		
	usuario_establece_precio_fijo = models.ForeignKey(User,on_delete = models.PROTECT,null=True,blank = True,related_name = "usuario_establece_precio_fijo")																							 	
	usuario_cancela = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True)
"""
	@classmethod
	def nuevo_empeno(self,sucursal,tp,caja,usuario,avaluo,mutuo,fecha_vencimiento,cliente,nombre_cotitular,apellido_paterno,apellido_materno,plazo,fecha_vencimiento_real,estatus,folio,tm):

		boleta = self.objects.create(folio = folio,tipo_producto = tp,caja = caja,usuario = usuario,avaluo = avaluo,mutuo = mutuo,fecha = timezone.now(),fecha_vencimiento = fecha_vencimiento,cliente = cliente,nombre_cotitular = nombre_cotitular,apellido_p_cotitular = apellido_paterno,apellido_m_cotitular = apellido_materno,plazo = plazo,sucursal = sucursal,mutuo_original = mutuo,fecha_vencimiento_real = fecha_vencimiento_real,estatus = estatus,almacenaje =  sucursal.fn_get_almacenaje(tp.id), interes = sucursal.fn_get_interes(tp.id),iva = sucursal.fn_get_iva(tp.id))
				
		return boleta	
			
	def forzar_desempeno(self,importe_desempeno):

		if int(importe_desempeno) < 0:
			return [False,"El importe debe ser mayor a cero."]

		# validacion 1: Validamos que la boleta este en estatus almoneda o remate
		if  self.estatus.id != 3 and self.estatus.id != 5:
			return [False,"La boleta debe estar en estatus Almoneda o Remate"]

		if self.plazo.id != 2:
			return [False,"Esta opciones solo esta disponible para boletas de plazo semanal"]

		try:
			with transaction.atomic():
				# Si cuenta con comisiones de PG sin pagar, las ponemos en cero
				pagos = Pagos.objects.filter(boleta = self,tipo_pago__id = 2,pagado = "N")
				for p in pagos:
					p.importe = 0
					p.save()

				# dividimo el nuevo importe para desempeno entre el numero de pagos pendientes
				pagos = Pagos.objects.filter(boleta = self,pagado = "N").exclude(importe = 0)
				nvo_importe = int(importe_desempeno/pagos.count())
				if nvo_importe == 0:	
					nvo_importe = 1

				for p in pagos:
					p.importe = nvo_importe
					p.save()
				return [True,""]
		except:
			transaction.set_rollback(True)
			return [False,"Error al actualizar la información."]


	#funcion que calcula el refrendo de los proximos pagos de una boleta consderando el mutuo actual y los porcentajes de interes
	#que se tenian al momento de hacer el empeño.	
	def fn_calcula_refrendo(self):
		
		p_almacenaje = decimal.Decimal(self.almacenaje)/decimal.Decimal(100)
		p_interes = decimal.Decimal(self.interes)/decimal.Decimal(100)
		p_iva = decimal.Decimal(self.iva)/decimal.Decimal(100)

		almacenaje = 0.00
		interes = 0.00
		iva=0.00
		refrendo = 0.00

		respuesta = []

		almacenaje = (decimal.Decimal(self.mutuo) * p_almacenaje)
		interes = (decimal.Decimal(self.mutuo) * p_interes)
		iva = ((almacenaje+interes) * p_iva)
		refrendo = round(almacenaje + interes + iva)
		respuesta.append({"estatus":"1","almacenaje":almacenaje,"interes":interes,"iva":iva,"refrendo":refrendo})
		
		return respuesta


	#funcion para calcular el refrendo, en base al nuevo mutuo
	#se usa para la simulacion
	#para calcular el mutuo actual, revisar la funcion fn_calcula_refrendo
	def fn_simula_calcula_refrendo(self,mutuo):
		p_almacenaje = decimal.Decimal(self.almacenaje)/decimal.Decimal(100)
		p_interes = decimal.Decimal(self.interes)/decimal.Decimal(100)
		p_iva = decimal.Decimal(self.iva)/decimal.Decimal(100)

		almacenaje = 0.00
		interes = 0.00
		iva=0.00
		refrendo = 0.00

		respuesta = []

		almacenaje = (decimal.Decimal(mutuo) * p_almacenaje)
		interes = (decimal.Decimal(mutuo) * p_interes)
		iva = ((almacenaje+interes) * p_iva)
		refrendo = round(almacenaje + interes + iva)
		respuesta.append({"estatus":"1","almacenaje":almacenaje,"interes":interes,"iva":iva,"refrendo":refrendo})		
		return respuesta

	def fn_simula_calcula_refrendo_2(mutuo,sucursal,id_tipo_producto):

		#cie = Configuracion_Interes_Empeno.objects.get(sucursal = sucursal)

		if id_tipo_producto == 1:
			p_almacenaje = decimal.Decimal(sucursal.fn_get_almacenaje(1))/decimal.Decimal(100)
			p_interes = decimal.Decimal(sucursal.fn_get_interes(1))/decimal.Decimal(100)
			p_iva = decimal.Decimal(sucursal.fn_get_iva(1))/decimal.Decimal(100)
		if id_tipo_producto == 2:
			p_almacenaje = decimal.Decimal(sucursal.fn_get_almacenaje(2))/decimal.Decimal(100)
			p_interes = decimal.Decimal(sucursal.fn_get_interes(2))/decimal.Decimal(100)
			p_iva = decimal.Decimal(sucursal.fn_get_iva(3))/decimal.Decimal(100)

		if id_tipo_producto == 3:
			p_almacenaje = decimal.Decimal(sucursal.fn_get_almacenaje(3))/decimal.Decimal(100)
			p_interes = decimal.Decimal(sucursal.fn_get_interes(3))/decimal.Decimal(100)
			p_iva = decimal.Decimal(sucursal.fn_get_iva(3))/decimal.Decimal(100)


		almacenaje = 0.00
		interes = 0.00
		iva=0.00
		refrendo = 0.00

		respuesta = []

		almacenaje = (decimal.Decimal(mutuo) * p_almacenaje)
		interes = (decimal.Decimal(mutuo) * p_interes)
		iva = ((almacenaje+interes) * p_iva)
		refrendo = round(almacenaje + interes + iva)
		respuesta.append({"estatus":"1","almacenaje":almacenaje,"interes":interes,"iva":iva,"refrendo":refrendo})		
		return respuesta

	def fn_get_numero_abonos(self):
		numero_abonos = Abono.objects.filter(boleta = self).count()
		return int(numero_abonos)


	#funcion que regresa un diccionario con los valores "min_semanas" y "max_semanas"
	# el min de semanas es el mino de semanas a refrendar por la boleta
	# el max de semanas es el maximo de semanas a regrendar permitidas por la boleta.
	# aplica solo para boletas semanales.
	def fn_get_min_y_max_semanas_a_pagar(self):
		
		max_semanas_a_refrendar = 0
		min_semanas_a_refrendar = 0

		#consultamos el numero de pagos que estan vencidos y sin pagar de la boleta, excluyendo las comision de periodo de gracia (tipo 2)
		num_pagos_vencidos = Pagos.objects.filter(boleta = self, vencido = 'S',pagado = "N").exclude(tipo_pago__id = 2).count()
		
		#si no tiene pagos vencidos.
		if num_pagos_vencidos == 0:
			#buscamos el proximo pago que no este vencido ni pagado y que sea refrendo o refrendo pg
			id_proximo_pago = Pagos.objects.filter(boleta = self, vencido = "N",pagado = "N").exclude(tipo_pago__id = 2).aggregate(Min("id"))["id__min"]
		
			prox_pago = Pagos.objects.get(id = id_proximo_pago)

			#validamos si el dia actual esta dentro del rango de este pago.
			today = datetime.combine(date.today(),time.min)


			dif_dias = abs((today - prox_pago.fecha_vencimiento_real).days)


			#Si la diferencia entre hoy y la fecha de vencimiento real, es mayor a 6, quiere decir que el dia de
			#hoy aun es parte de alguna semana de pago.
			if dif_dias > 6 :
				
				if dif_dias == 7:#si es 7
					#si es el dia en que se genero la boleta se cobra

					if datetime.combine(self.fecha,time.min) == today :
						max_semanas_a_refrendar = 1
						min_semanas_a_refrendar = 1
					else:
						max_semanas_a_refrendar = 0
						min_semanas_a_refrendar = 0
				else:
					max_semanas_a_refrendar = 0
					min_semanas_a_refrendar = 0
				#if prox_pago.pagado == "N":
				#	max_semanas_a_refrendar = 1
				#	min_semanas_a_refrendar = 1
				#else:
				#	max_semanas_a_refrendar = 0
				#	min_semanas_a_refrendar = 0
			#si la diferencia entre hoy y la fecha de vencimiento real, es menor o igual a 7, quiere edcir que el dia de 
			#hoy si pertenece a una semana de pago
			else:
				if prox_pago.pagado == "S":
					max_semanas_a_refrendar = 0
					min_semanas_a_refrendar = 0
				else:
					max_semanas_a_refrendar = 1
					min_semanas_a_refrendar = 1

		elif num_pagos_vencidos > 0 and num_pagos_vencidos <= 4:
			min_semanas_a_refrendar = 1
			max_semanas_a_refrendar = num_pagos_vencidos + 1
		else:
			min_semanas_a_refrendar = num_pagos_vencidos - 3
			max_semanas_a_refrendar = num_pagos_vencidos + 1

		return {"max_semanas_a_refrendar":max_semanas_a_refrendar,"min_semanas_a_refrendar":min_semanas_a_refrendar}

	#funcion que regresa true en caso de que la boleta acepte refrendo (es porque esta en estatus 1-abierta, 3-almoneda o 5-remate)
	#o false si no acepta refrendo.
	def fn_acepta_refrendo(self):
		if self.estatus.id == 1 or self.estatus.id == 3 or self.estatus.id == 5:
			return True
		else:
			return False

	def fn_get_comision_pg(self):		
		#sumamos todas las comisiones de periodos de gracia que no han sido pagados
		importe_cpg = Pagos.objects.filter(boleta = self,pagado = "N", tipo_pago__id = 2).aggregate(Sum("importe"))["importe__sum"]
		if importe_cpg == None:
			importe_cpg = 0
		return importe_cpg

	def fn_get_dias_vencida(self):
		#si es estatus almoneda o remate, regresamos el tiempo que lleva vencida la boleta.
		if self.estatus.id == 3 or self.estatus.id == 5:
			today = datetime.combine(date.today(),time.max)
			dias_vencido = (today-self.fecha_vencimiento).days

			#no deberia pasar que sea negativo, pero por si acaso
			if dias_vencido < 0:
				dias_vencido = 0

			return dias_vencido
		else:
			return 0 

	#este para plazo semanal
	def fn_simula_proximos_pagos(self,semanas_a_refrendar):
		min_semanas = self.fn_get_min_y_max_semanas_a_pagar()["min_semanas_a_refrendar"]
		max_semanas = self.fn_get_min_y_max_semanas_a_pagar()["max_semanas_a_refrendar"]

		#si el numero de semanas esta fuera de rango
		if semanas_a_refrendar < min_semanas or semanas_a_refrendar > max_semanas:
			return None

		#despues de aplicar un refrendo, deben quedar siempre 4 pagos sin pagar, sin importar si estan vencidos o no.

		#si la boleta esta vencida
		if self.estatus.id ==3 or self.estatus.id ==5:					
			pagos_que_continuan = Pagos.objects.filter(boleta = self, pagado = "N").exclude(tipo_pago__id = "2").order_by("id")[semanas_a_refrendar:max_semanas]
			#Solo puede haber 4 pagos maximos sin pagar despues de aplicar el refrendo,			
			num_nuevos_pagos = 4 - pagos_que_continuan.count()
		else:
			#en toda boleta no venvida, debera haber 4 semanas sin pagar.
			pagos_que_continuan = Pagos.objects.filter(boleta = self, pagado = "N").exclude(tipo_pago__id = "2").order_by("id")[semanas_a_refrendar:]
			#por cada semana a refrendar vamos a generar un nuevo pago.
			num_nuevos_pagos = semanas_a_refrendar
		#creamos una lista para almacenar los nuevos pagos
		nuevos_pagos = []
		ultima_fecha_vencimiento = None
		#se agregan los pagos que continuan a la lista de nuevos pagos
		#aunq estos ya estan vencidos, se mostraran en pantalla de simulacion de proximos pagos
		for p in pagos_que_continuan:				
			ultima_fecha_vencimiento = p.fecha_vencimiento						
			nuevos_pagos.append(p.fecha_vencimiento.strftime('%Y-%m-%d'))
		if ultima_fecha_vencimiento == None:
			id_ultimo_abono = Pagos.objects.filter(boleta = self, pagado = "N").exclude(tipo_pago__id = "2").aggregate(Max("id"))["id__max"]
			ultima_fecha_vencimiento = Pagos.objects.get(id=id_ultimo_abono).fecha_vencimiento

		seven_days = timedelta(days = 7)
		fecha_real = ultima_fecha_vencimiento

		for n in range(0,num_nuevos_pagos):			
			
			fecha_real = datetime.combine((fecha_real+seven_days),time.min)				
			ultima_fecha_vencimiento = fecha_real
			ultima_fecha_vencimiento = fn_fecha_vencimiento_valida(ultima_fecha_vencimiento)
			nuevos_pagos.append(ultima_fecha_vencimiento.strftime('%Y-%m-%d'))
			
		return nuevos_pagos

	#si regresa false es que algo fallo, y no debemos continuar con la aplicacion del refrendo.
	@transaction.atomic
	def fn_paga_comision_pg(self,descuento,abono):
		resp = []
		hoy = date.today()
		hoy = datetime.combine(hoy,time.min)

		#si el estatus es diferente de almoneda o remate y se va a aplicar un decuento es que algo salio mal.
		#ya que no es posible aplicar descuento a una boleta que no esta en almoneda o en remate.
		if self.estatus.id != 3 and self.estatus.id != 5:
			if int(descuento) > 0:				
				resp.append(False)
				resp.append("No es posible aplicar descuento a la boleta.")
				return resp
			else:
				resp.append(True)
				return resp

		#SI ESTAMOS EN ESTE PUNTO ES QUE LA BOLETA SI ESTA EN ALMONEDA O REMATE.
		#obtenemos todos las comisiones de Pg que no han sido pagadoas.
		comision_pg = Pagos.objects.filter(boleta = self,tipo_pago__id = 2,pagado = "N")

		#en caso de quela boleta tenga inconsistencias entre el numero de dias vencidos y el nuero de comisiones pg no pagadas.
		#if self.fn_get_dias_vencida() != comision_pg.count():
		#	resp.append(False)
		#	resp.append("La boleta presenta inconcistencias entre los dias vencidos y el importe de comisiones pg.")
		#	return resp

		pagos_no_pagados = Pagos.objects.filter(boleta = self,pagado = "N")
		importe_comision_pg = comision_pg.aggregate(Sum("importe"))["importe__sum"]

		if importe_comision_pg == None:
			importe_comision_pg = 0		

		if float(descuento) > 0:
			#para aplicar descuento debe tener mas de 0 y 3 o menos dias vencidos			
			if comision_pg.count() > 3:				
				resp.append(False)
				resp.append("No es posible aplicar descuento a la boleta. Tiene más de tres dias vencida.")
				
				return resp

			#validamos que el descuento cubra todas las comisiones de periodo de gracia.
			if float(descuento) < float(importe_comision_pg):				
				resp.append(False)
				resp.append("El importe de descuento no cubre las comisiones de periodo de gracia.")
				return resp



		if comision_pg.exists():			

			
			if descuento == 0:					
				try:
					for cpg in comision_pg:
						cpg.pagado = "S"
						cpg.fecha_pago=timezone.now()
						cpg.save()								

						#creamos la relacion entre el abono y los pagos
						rel=Rel_Abono_Pago()
						rel.abono=abono
						rel.pago=cpg
						rel.save()
				except Exception as e:	
					resp.append(False)				
					return resp

			else:				
				#al aplicar descuento, no se cobran las comisiones pg,
				#por lo tanto se eliminan, pero en cas de querer cancelar el refrendo
				#se almacenan en la tabla tempora Pagos_Com_Pg_No_Usados por un dia
				#osea que un refrendo solo se puede cancelar el mismo dia en que se aplico.				
				try:
					for cpg in comision_pg:
						resp_com_pg = Pagos_Com_Pg_No_Usados()
						resp_com_pg.tipo_pago = cpg.tipo_pago
						resp_com_pg.boleta = cpg.boleta
						resp_com_pg.fecha_vencimiento = cpg.fecha_vencimiento
						resp_com_pg.almacenaje = cpg.almacenaje
						resp_com_pg.interes = cpg.interes
						resp_com_pg.iva = cpg.iva
						resp_com_pg.importe = cpg.importe
						resp_com_pg.vencido = cpg.vencido
						resp_com_pg.pagado = cpg.pagado
						resp_com_pg.fecha_pago = cpg.fecha_pago
						resp_com_pg.fecha_vencimiento_real = cpg.fecha_vencimiento_real
						resp_com_pg.abono = abono
						resp_com_pg.save()
					comision_pg.delete()															
				except Exception as e:							
					resp.append(False)				
					return resp

		resp.append(True)				
		return resp

	#el importe a pagos que aqui se recibe es el importe despues de haber descontado 
	#el importe a comision de PG (en caso de que los tenga.)
	@transaction.atomic
	def fn_salda_pagos(self,numero_semanas_a_pagar,importe_a_pagos,abono):

		resp = []

		#el importe a pagos debe ser mayor o igual a el importe que corresponde al numero de semanas a pagar
		comision_pg = Pagos.objects.filter(boleta = self, pagado = "N",tipo_pago__id = 2)
		#si existe comision Pg, es que algo salio mal, y no debemos continuar
		if comision_pg.exists():
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas. No se liquidaron correctamente las comisiones de periodo de gracia.")
			return resp

		#validamos que la boleta tenga la fecha de vencimiento y fecha de vencimiento real correctas
		if (self.fecha_vencimiento-self.fecha_vencimiento_real).days !=0 and (self.fecha_vencimiento-self.fecha_vencimiento_real).days !=1:
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas. La fecha de vencimiento de la boleta es diferente a la fecha de vencimiento real.")
			return resp


		#buscamos los pagos que se van a saldar
		pagos = Pagos.objects.filter(boleta = self,pagado = "N").exclude(tipo_pago__id = 2)
		#validamos que los pagos tengan la fecha de vencimiento real correcta
		for p in pagos:
			if (p.fecha_vencimiento - p.fecha_vencimiento_real).days != 0 and (p.fecha_vencimiento - p.fecha_vencimiento_real).days != 1:
				resp.append(False)
				resp.append("Error al pagar las semanas indicadas. La fecha de vencimiento es diferente a la fecha de vencimiento real.")
				return resp

		#validamos que las semanas a pagar sean correctas
		sem_max_min = self.fn_get_min_y_max_semanas_a_pagar()

		if sem_max_min['max_semanas_a_refrendar'] == 0:
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas. El numero maximo de semanas a pagar es cero.")
			return resp

		if numero_semanas_a_pagar > sem_max_min['max_semanas_a_refrendar'] or numero_semanas_a_pagar < sem_max_min['min_semanas_a_refrendar']:
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas. El numero de semanas a pagar no es correcto.")
			return resp

		#sin contar los pagos por comision pg
		importe_semanal = Pagos.objects.filter(boleta = self, pagado = "N").exclude(tipo_pago__id = 2).aggregate(Max("importe"))["importe__max"]

		#si no encuentra el importe semanal es porque algo fallo.
		if importe_semanal == None:			
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas.")
			return resp
			

		importe_pagos = int(importe_semanal) * numero_semanas_a_pagar

		#validamos que el importe a pagos (ya descontamos el importe de comision pg)
		#cubra al 100% el importe a pagos.
		#de lo contrario regresa false.
		if importe_a_pagos < importe_pagos:		
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas. El importe destinado a refrendos no cubre el numero de semanas indicadas.")
			return resp

		#si paso las validaciones anteriores, aplicamos el abono.

		fecha_vencimiento_aux = self.fecha_vencimiento 
		fecha_vencimiento_real_aux = self.fecha_vencimiento_real 

		#obtenemos los proximos pagos.
		nuevos_pagos = self.fn_simula_proximos_pagos(numero_semanas_a_pagar)


		#buscamos los pagos a los que afectara.
		pagos = Pagos.objects.filter(boleta = self,pagado = "N").exclude(tipo_pago__id = 2).order_by("id")[:numero_semanas_a_pagar]

		#se obtiene la ultima fecha de vencimiento real de refrendo o refrendo pg
		#ya que desde ahi se empieza a contar la fecha de vencimiento real de  los nuevos pagos			
		fecha_vencimiento_real = Pagos.objects.filter(boleta = self,pagado = "N").exclude(tipo_pago__id = 2).aggregate(Max("fecha_vencimiento_real"))["fecha_vencimiento_real__max"]

		try:
			for p in pagos:
				p.pagado = "S"
				p.tipo_pago = Tipo_Pago.objects.get(id = 1)#cambiamos el pago a refrendo (esto porque de lo contrario fallaria en el job de pagos vencidos.)
				p.fecha_pago = timezone.now()
				p.save()

				#creamos la relacion entre el abono y los pagos
				rel=Rel_Abono_Pago()
				rel.abono=abono
				rel.pago=p
				rel.save()

			tp_refrendo = Tipo_Pago.objects.get(id = 1)

			resp_cr = self.fn_calcula_refrendo()
			
			almacenaje=decimal.Decimal(resp_cr[0]["almacenaje"])/decimal.Decimal(4.00)
			interes=decimal.Decimal(resp_cr[0]["interes"])/decimal.Decimal(4.00)
			iva=decimal.Decimal(resp_cr[0]["iva"])/decimal.Decimal(4.00)
			refrendo=round(decimal.Decimal(resp_cr[0]["refrendo"])/decimal.Decimal(4.00))

			#creamos los nuevos pagos.
			for np in nuevos_pagos:	
				pago = Pagos.objects.filter(boleta = self,pagado = "N",fecha_vencimiento = datetime.strptime(np,'%Y-%m-%d')).exclude(tipo_pago__id = 2)
				
				
				if not pago.exists():
					#la fecha de vencimiento real se incrementa de a 7 dias.
					fecha_vencimiento_real = fecha_vencimiento_real + timedelta(days = 7)
					pgo=Pagos()					
					pgo.tipo_pago=tp_refrendo
					pgo.boleta=self
					pgo.fecha_vencimiento = datetime.strptime(np,'%Y-%m-%d')
					pgo.almacenaje=almacenaje
					pgo.interes=interes
					pgo.iva=iva
					pgo.importe=refrendo
					pgo.vencido="N"
					pgo.pagado="N"
					pgo.fecha_vencimiento_real = fecha_vencimiento_real#datetime.strptime(np,'%Y-%m-%d')

					#en caso de cancelar el refrendo, necesitamos saber que semanas genero el refrendo.
					#para poder eliminarlas.
					pgo.abono = abono
					pgo.save()
				else:
					for p in pago:
						p.tipo_pago = tp_refrendo
						p.save()

				self.fecha_vencimiento = datetime.strptime(np,'%Y-%m-%d')
				self.fecha_vencimiento_real = fecha_vencimiento_real

			estatus_abierta = Estatus_Boleta.objects.get(id = 1)
			
			self.estatus = estatus_abierta
			self.save()

			#despues de haber aplicado el abono, validamos que la boleta este correcta.
			#validamos las fechas de vencimiento y vencimiento real de la boleta
			if (self.fecha_vencimiento-self.fecha_vencimiento_real).days !=0 and (self.fecha_vencimiento-self.fecha_vencimiento_real).days != 1:
				resp.append(False)
				resp.append("Error al pagar las semanas indicadas. No se pudo calcular la fecha de vencimiento de la boleta.")
				return resp

			pagos = Pagos.objects.filter(boleta = self,pagado = "N")

			for p in pagos:
				if (p.fecha_vencimiento - p.fecha_vencimiento_real).days != 0 and (p.fecha_vencimiento - p.fecha_vencimiento_real).days != 1:
					resp.append(False)
					resp.append("Error al pagar las semanas indicadas. No se pudo calcular la fecha de vencimiento de los proximos pagos.")
					return resp										


			resp.append(True)
			
			return resp
		except Exception as e:
			print(str(e))
			resp.append(False)
			resp.append("Error al pagar las semanas indicadas.")
			return resp

	@transaction.atomic
	def fn_abona_capital(self,importe_capital,abono):
		try:

			print("empezamos el abono a capital")
			#validamos que la boleta tenga como maximo numero de pagos 0
			#ya que de lo contrario, no puede abonar a capital.
			max_semanas_a_refrendar = self.fn_get_min_y_max_semanas_a_pagar()["max_semanas_a_refrendar"]
			
			if max_semanas_a_refrendar != 0:
				return False

			if type(importe_capital) != type(0):
				return False

			mutuo=self.mutuo
			mutuo=int(mutuo)-int(importe_capital)

			#actualizamos el mutuo del la boleta.
			self.mutuo=mutuo
			self.save()

			rel_cap = Rel_Abono_Capital()
			rel_cap.boleta = self
			rel_cap.abono = abono
			rel_cap.importe = importe_capital
			rel_cap.capital_restante = mutuo
			rel_cap.save()

			resp=self.fn_calcula_refrendo()

			almacenaje=decimal.Decimal(resp[0]["almacenaje"])/decimal.Decimal(4.00)
			interes=decimal.Decimal(resp[0]["interes"])/decimal.Decimal(4.00)
			iva=decimal.Decimal(resp[0]["iva"])/decimal.Decimal(4.00)
			refrendo=round(decimal.Decimal(resp[0]["refrendo"])/decimal.Decimal(4.00))		

			est_refrendo = Tipo_Pago.objects.get(id = 1)
			#buscamos los abonos no pagados y no vencidos para actualizar su importe en base al nuevo mutuo
			pagos_t=Pagos.objects.filter(pagado="N",tipo_pago=est_refrendo,boleta=self,vencido="N").order_by("id")


			#actualizamos el importe de los pagos con el nuevo refrendo.
			for pt in pagos_t:
				if mutuo!=0:
					pt.importe=refrendo
					pt.almacenaje=almacenaje
					pt.interes=interes
					pt.iva=iva
					pt.save()
				else:					
					#respaldamos los pagos no usados (por el desempeño) para en caso de cancelar el abono podramos restaurarlo.
					resp_pagos = Pagos_No_Usados()
					resp_pagos.tipo_pago = pt.tipo_pago
					resp_pagos.boleta = pt.boleta
					resp_pagos.fecha_vencimiento = pt.fecha_vencimiento
					resp_pagos.almacenaje = pt.almacenaje
					resp_pagos.interes = pt.interes
					resp_pagos.iva = pt.iva
					resp_pagos.importe = pt.importe
					resp_pagos.vencido = pt.vencido
					resp_pagos.pagado = pt.pagado
					resp_pagos.fecha_pago = pt.fecha_pago
					resp_pagos.fecha_vencimiento_real = pt.fecha_vencimiento_real
					resp_pagos.abono = pt.abono#el abono que genero el refrendo
					resp_pagos.abono_respaldo = abono
					resp_pagos.save()

					pt.delete()
					#marcamos la boleeta como desempeñada.
					desempenada=Estatus_Boleta.objects.get(id=4)
					self.estatus=desempenada
					self.mutuo=0
					self.refrendo=0
					self.save()
			return True
		except Exception as e:
			print(e)			
			return False


	def fn_calcula_precio_venta(self):
		#si se definio un precio de venta fijo, ese es el que regresa
		if self.precio_venta_fijo != 0:
			return self.precio_venta_fijo

		importe_venta=0.00

		porcentaje = Porcentaje_Sobre_Avaluo.objects.all().aggregate(Sum("porcentaje"))

		porce = 0;
		if porcentaje["porcentaje__sum"]!=None:
			porce = decimal.Decimal(porcentaje["porcentaje__sum"])

		importe_venta = decimal.Decimal(self.avaluo) + (decimal.Decimal(self.avaluo)*(decimal.Decimal(porce)/decimal.Decimal(100.00)))
		return importe_venta

	def fn_calcula_precio_apartado(self):	
		#si se definio un precio de venta fijo, ese es el que regresa
		if self.precio_venta_fijo != 0:
			return self.precio_venta_fijo
			
		importe_venta=0.00
		porcentaje=Porcentaje_Sobre_Avaluo.objects.all().aggregate(Sum("porcentaje_apartado"))
		porce=0;

		if porcentaje["porcentaje_apartado__sum"]!=None:
			porce=decimal.Decimal(porcentaje["porcentaje_apartado__sum"])

			importe_venta=decimal.Decimal(self.avaluo)+(decimal.Decimal(self.avaluo)*(decimal.Decimal(porce)/decimal.Decimal(100.00)))

		return importe_venta
	def fn_establece_precio_venta_y_apartado(self,importe,id_usuario):
		resp = []
		try:
			self.precio_venta_fijo = importe
			self.usuario_establece_precio_fijo = User.objects.get(id = id_usuario)
			self.save()
			resp.append(True)			
		except Exception as e:
			print("fn_establece_precio_venta_y_apartado:- " + str(e))
			resp.append(False)			
		return resp


	class Meta:
		unique_together=("folio",'sucursal',)

"""