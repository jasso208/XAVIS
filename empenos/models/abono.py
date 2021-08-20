from django.db import models
from django.db import transaction
from empenos.models.tipo_movimiento import Tipo_Movimiento
from seguridad.models.sucursal import Sucursal
from empenos.models.boleta_empeno import Boleta_Empeno
from django.utils import timezone
from django.contrib.auth.models import User
from empenos.models.cajas import Cajas

ESTATUS_ABONO = (
	('1','ACTIVO'),
	('2','CANCELADO'),
)
class Abono(models.Model):
	folio = models.CharField(max_length=7,null=True)
	tipo_movimiento = models.ForeignKey(Tipo_Movimiento,on_delete=models.PROTECT,null=True,blank=True)
	sucursal = models.ForeignKey(Sucursal,on_delete=models.PROTECT,null=True,blank=True)	
	fecha = models.DateTimeField(default=timezone.now)
	usuario = models.ForeignKey(User,on_delete=models.PROTECT,related_name = "usuario_alta_abono")
	importe = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)	
	caja = models.ForeignKey(Cajas,on_delete=models.PROTECT,blank=True,null=True)
	boleta = models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT,blank=True,null=True)
	estatus = models.CharField(choices = ESTATUS_ABONO,max_length = 10,default = "ACTIVO")
	usuario_cancela = models.ForeignKey(User,on_delete = models.PROTECT,null = True,blank = True,related_name = "usuario_cancela_abono")

"""
	#funcion para cancelar abono
	@transaction.atomic
	def fn_cancela_abono(self,usuario):
		hoy = datetime.combine(date.today(),time.min)
		fecha_abono = datetime.combine(self.fecha,time.min)

		resp = []

		if hoy != fecha_abono:
			resp.append(False)
			resp.append("El abono no puede ser cancelado ya que no es del dia de hoy.")
			return resp

		abonos_posteriores = Abono.objects.filter(boleta = self.boleta, id__gt = self.id)

		if abonos_posteriores.exists():
			resp.append(False)
			resp.append("El abono no puede ser cancelado ya que existe un abono posterior al que intenta cancelar.")
			return resp

		if self.boleta.estatus_anterior == None:
			resp.append(False)
			resp.append("El abono no puede ser cancelado ya que no es posible calcular el estatus de boleta anterior.")
			return resp

		if self.boleta.fecha_vencimiento_anterior == None or self.boleta.fecha_vencimiento_real_anterior == None:
			resp.append(False)
			resp.append("El abono no puede ser cancelado ya que no es posible calcular la fecha de vencimiento anterior.")
			return resp



		#si llegamos a este punto es que el abono si se puede cancelar.

		#eliminamos los pagos que se generaron al aplicar el refrendo
		Pagos.objects.filter(abono = self).delete()
		#regresamos el estatus de la boleta.
		self.boleta.fecha_vencimiento = self.boleta.fecha_vencimiento_anterior
		self.boleta.fecha_vencimiento_real = self.boleta.fecha_vencimiento_real_anterior
		self.boleta.estatus = self.boleta.estatus_anterior
		self.boleta.save()

		#obtenemos las comisiones pg a las que se le aplico descuento con el abono.
		pagos_pg = Pagos_Com_Pg_No_Usados.objects.filter(abono = self)

		if pagos_pg.exists():
			for p in pagos_pg:			
				pago = Pagos()
				pago.tipo_pago = p.tipo_pago
				pago.boleta = p.boleta
				pago.fecha_vencimiento = p.fecha_vencimiento
				pago.almacenaje = p.almacenaje
				pago.interes = p.interes
				pago.iva = p.iva
				pago.importe = p.importe
				pago.vencido = p.vencido
				pago.pagado = "N"
				pago.fecha_pago = None
				pago.fecha_vencimiento_real = p.fecha_vencimiento_real
				pago.save()

			Pagos_Com_Pg_No_Usados.objects.filter(abono = self).delete()

		#obtenemos los pagos no usados en caso de desempeño y los restauramos
		pagos_resp = Pagos_No_Usados.objects.filter(abono_respaldo = self)
		if pagos_resp.exists():
			for p in pagos_resp:			
				pago = Pagos()
				pago.tipo_pago = p.tipo_pago
				pago.boleta = p.boleta
				pago.fecha_vencimiento = p.fecha_vencimiento
				pago.almacenaje = p.almacenaje
				pago.interes = p.interes
				pago.iva = p.iva
				pago.importe = p.importe
				pago.vencido = p.vencido
				pago.pagado = "N"
				pago.fecha_pago = None
				pago.fecha_vencimiento_real = p.fecha_vencimiento_real
				pago.abono = p.abono
				pago.save()

			Pagos_No_Usados.objects.filter(abono = self).delete()

		#eliminamos los pagos que fueron generados por el abono que se esta cancelando.
		Pagos.objects.filter(abono = self).delete()


		#validamos si afecto abono a capital, y lo regresamos.
		if Rel_Abono_Capital.objects.filter(abono = self).exists():			
			self.boleta.mutuo = self.boleta.mutuo + Rel_Abono_Capital.objects.get(abono = self).importe			
			self.boleta.save()
			Rel_Abono_Capital.objects.filter(abono = self).delete()

		#calculamos el refrendo en base al nuevo mutuo
		r = self.boleta.fn_calcula_refrendo()


		almacenaje = decimal.Decimal(r[0]["almacenaje"])/decimal.Decimal(4.00)
		interes = decimal.Decimal(r[0]["interes"])/decimal.Decimal(4.00)
		iva = decimal.Decimal(r[0]["iva"])/decimal.Decimal(4.00)
		refrendo = round(decimal.Decimal(r[0]["refrendo"])/decimal.Decimal(4.00))

		self.boleta.refrendo = math.ceil((refrendo * 4.00))
		self.boleta.save()


		#en cso d que se haya abonado a capital, aplicamos rollback a el importe de refrendo semanal.
		for pago in Pagos.objects.filter(boleta = self.boleta,pagado = "N").exclude(tipo_pago__id = 2):
			pago.almacenaje  = almacenaje
			pago.interes = interes
			pago.iva = iva
			pago.importe = refrendo
			pago.save()

		#obtenemos los pagos (afecta a comisionpg, refrendo y refrendo pg) que afecto el abono y los regresamos a no pagados
		rap = Rel_Abono_Pago.objects.filter(abono = self)		

		
		for p in rap:
			pago = p.pago
			pago.pagado = "N"
			pago.fecha_pago = None		
			pago.save()

		Rel_Abono_Pago.objects.filter(abono = self).delete()

		#los pagos que tengan fecha de vencimiento mayor a la fech de vencimiento de la boleta
		#son considerados Refrendo pg
		for p in Pagos.objects.filter(boleta = self.boleta,pagado = "N").exclude(tipo_pago__id = 2):
			if p.fecha_vencimiento > self.boleta.fecha_vencimiento:
				
				p.tipo_pago = Tipo_Pago.objects.get(id=3)
				p.save()

		self.estatus = "CANCELADO"
		self.usuario_cancela = usuario
		self.importe = 0

		self.save()

		return resp

"""