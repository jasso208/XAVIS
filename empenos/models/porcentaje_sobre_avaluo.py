from django.db import models
#al momendo de anunciar un producto para la venta piso, 
#se le aumenta un % sobre el avaluo, ese porcentaje es configurable en esta tabla.
#es por negocio
#solo debe existir un registro.
class Porcentaje_Sobre_Avaluo(models.Model):
	porcentaje=models.DecimalField(max_digits = 20,decimal_places = 2)#este es el procentaje para venta
	porcentaje_apartado=models.DecimalField(max_digits = 20, decimal_places = 2)#es el porcentaje para apartado

	#porcentaje=models.IntegerField()#este es el procentaje para venta
	#porcentaje_apartado=models.IntegerField()#es el porcentaje para apartado