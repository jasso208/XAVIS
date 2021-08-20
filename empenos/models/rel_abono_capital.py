#cuando un abono afecta a capital, aqui almacenamos a que boleta le afecto el capital y el importe.
from django.db import models
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.abono import Abono
class Rel_Abono_Capital(models.Model):
	abono=models.ForeignKey(Abono,on_delete=models.PROTECT)
	boleta=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT)
	importe=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
	capital_restante=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)#cuando se afecte el capital, aqui almacenamos el historial de como quedo al aplicar el abono.
