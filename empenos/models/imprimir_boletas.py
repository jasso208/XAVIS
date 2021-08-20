from django.db import models
from empenos.models.boleta_empeno import Boleta_Empeno
from django.contrib.auth.models import User

##se llena al generar un empeño
#lo usamos como auxiliar para imprimir las boletas.
class Imprimir_Boletas(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT)
	reimpresion=models.IntegerField(default=0)#cuando tenga 1 es que es reimpresion y se le cobra 10 pesos.
