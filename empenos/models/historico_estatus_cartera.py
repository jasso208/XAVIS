from django.db import models
from seguridad.models.sucursal import Sucursal
from django.utils import timezone

#almacenamos el estatus de cartera a diario
class Historico_Estatus_Cartera(models.Model):
	sucursal = models.ForeignKey(Sucursal,on_delete = models.PROTECT)
	fecha = models.DateTimeField(default = timezone.now())
	num_boletas_activas = models.IntegerField()
	num_boletas_almoneda = models.IntegerField()
	num_boletas_remate = models.IntegerField()
	importe_mutuo_activas = models.DecimalField(decimal_places = 2,max_digits = 26)
	importe_mutuo_almoneda = models.DecimalField(decimal_places = 2,max_digits = 26)
	importe_mutuo_remate = models.DecimalField(decimal_places = 2,max_digits = 26)
	importe_avaluo_activas = models.DecimalField(decimal_places = 2,max_digits = 26)
	importe_avaluo_almoneda = models.DecimalField(decimal_places = 2,max_digits = 26)
	importe_avaluo_remate = models.DecimalField(decimal_places = 2,max_digits = 26)


	class Meta:
		unique_together = ("sucursal","fecha")