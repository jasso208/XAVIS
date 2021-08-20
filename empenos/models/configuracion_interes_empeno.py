from django.db import models
from seguridad.models.sucursal import Sucursal
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

class Configuracion_Interes_Empeno(models.Model):
	sucursal = models.OneToOneField(Sucursal,on_delete = models.PROTECT)
	almacenaje_oro = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	interes_oro = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	iva_oro = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	almacenaje_plata = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	interes_plata = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	iva_plata = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	almacenaje_prod_varios = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	interes_prod_varios = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	iva_prod_varios = models.DecimalField(max_digits = 20,decimal_places = 2,default = 0.00)
	usuario_modifica = models.ForeignKey(User,on_delete=models.PROTECT)
	fecha_modificacion = models.DateTimeField(default = timezone.now)

	#si no encuentra la condiguracion, regresa false para indicar que no la tiene capturada.
	def fn_get_configuracion_interes_empeno(sucursal):
		try:
			return Configuracion_Interes_Empeno.objects.get(sucursal = sucursal)
		except:
			return False

	def fn_set_configuracion_interes_empeno(sucursal,almacenaje_oro,interes_oro,iva_oro,almacenaje_plata,interes_plata,iva_plata,almacenaje_prod_varios,interes_prod_varios,iva_prod_varios,usuario_modifica):
		try:
			cie = Configuracion_Interes_Empeno.objects.get(sucursal = sucursal)
			
			cie.almacenaje_oro=almacenaje_oro
			cie.save()
		except Exception as e:
			print(e)
			#cie = fn_actualiza_porcentaje_mutuo()

		
		try:
			cie.almacenaje_oro = almacenaje_oro
			cie.interes_oro = interes_oro
			cie.iva_oro = iva_oro
			cie.almacenaje_plata = almacenaje_plata
			cie.interes_plata = interes_plata
			cie.iva_plata = iva_plata
			cie.almacenaje_prod_varios = almacenaje_prod_varios
			cie.interes_prod_varios = interes_prod_varios
			cie.iva_prod_varios = iva_prod_varios
			cie.usuario_modifica = usuario_modifica
			cie.fecha_modificacion = date.today()
			cie.save()
			return True
		except:
			return False

