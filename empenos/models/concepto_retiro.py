from django.db import models
from seguridad.models.sucursal import Sucursal
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth.models import User
import calendar
SI_NO=(
	('1','SI'),
	('2','NO'),
)

class Concepto_Retiro(models.Model):
	concepto = models.CharField(max_length = 40,null = False)
	sucursal = models.ForeignKey(Sucursal,on_delete = models.PROTECT,blank=True,null=True,related_name = "sucursal_origen")
	importe_maximo_retiro = models.PositiveIntegerField()	
	fecha_alta = models.DateTimeField(default = timezone.now)
	fecha_modificacion = models.DateTimeField(default = timezone.now)
	usuario_ultima_mod = models.ForeignKey(User,on_delete = models.PROTECT)
	activo = models.CharField(choices=SI_NO,max_length=2,default="SI")
	sucursal_destino = models.ForeignKey(Sucursal,on_delete = models.PROTECT,null = True,blank = True,related_name = "sucursal_destino")#en caso de que sea un concepto para traspaso, esta es la sucursal a la que va dirigido

	def __str__(self):
		return str(self.id)+' '+self.concepto+' '+str(self.importe_maximo_retiro)
"""
	def fn_nuevo_concepto(id_sucursal,id_usuario,importe,concepto,id_sucursal_destino):	

		try:
			if concepto == "":
				return False

			if int(importe) < 0 or int(importe) == 0:
				return False

			sucursal = Sucursal.objects.get(id = int(id_sucursal))
			sucursal_destino = None
			if Sucursal.objects.filter(id = int(id_sucursal_destino)).exists():
				sucursal_destino = Sucursal.objects.get(id = int(id_sucursal_destino))	

			usuario = User.objects.get(id = int(id_usuario))
			Concepto_Retiro.objects.create(activo = 1, concepto = concepto.upper(),sucursal = sucursal,importe_maximo_retiro = importe,usuario_ultima_mod = usuario,sucursal_destino = sucursal_destino)
			return True
		except Exception as e:
			print(e)
			return False

	def fn_get_conceptos(id_sucursal):

		return Concepto_Retiro.objects.filter(sucursal__id = int(id_sucursal),activo="1")

	def fn_delete_concepto(id_concepto,id_usuario):
		try:
			usuario = User.objects.get(id = int(id_usuario))

			concepto = Concepto_Retiro.objects.get(id = int(id_concepto))
			concepto.activo = 2
			concepto.usuario_ultima_mod = usuario
			concepto.fecha_modificacion = datetime.now()
			concepto.save()

			return True;
		except Exception as e:
			
			return False;

	def fn_update_importe_maximo_retiro(id_concepto,importe_maximo_retiro,id_usuario):
		try:

			if int(importe_maximo_retiro) < 0:
				return False

			if int(importe_maximo_retiro) == 0:
				return False
				
			usuario = User.objects.get(id = int(id_usuario))
			concepto = Concepto_Retiro.objects.get(id=int(id_concepto))
			concepto.importe_maximo_retiro = importe_maximo_retiro
			concepto.usuario_ultima_mod=usuario
			concepto.fecha_modificacion=datetime.now()
			concepto.save()
			
			return True
		except Exception as e:			
			print(e)
			return False

	def fn_saldo_concepto(self):		
		#obtenemos la fecha inicial y fecha final del mes en curso
		fecha = timezone.now()
		rangos_fecha = calendar.monthrange(fecha.year , fecha.month)

		mes = rangos_fecha[1]
		fecha_inicial = datetime(int(fecha.year),int(fecha.month),1,0,0)
		fecha_final = datetime(fecha.year,fecha.month,mes,0,0)
		fecha_inicial = datetime.combine(fecha_inicial,time.min)
		fecha_final = datetime.combine(fecha_final,time.max)

		#obtenemos todos los retiros pertenecientes al consepto consultado
		re = Retiro_Efectivo.objects.filter(concepto = self,fecha__range = (fecha_inicial,fecha_final)).aggregate(Sum("importe"))
		
		total_retirado = 0
		if re["importe__sum"] != None:
			total_retirado = re["importe__sum"]
		else:
			total_retirado = 0

		#retornamos la diferencia entre el importe maximo y el total retirado
		#para saber cuando saldo le queda a este concepto
		return int(self.importe_maximo_retiro) - int(total_retirado)
"""