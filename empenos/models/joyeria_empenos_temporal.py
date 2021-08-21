from django.db import models
from empenos.models import kilataje
from empenos.models.empenos_temporal import Empenos_Temporal
from empenos.models.kilataje import Kilataje

class Joyeria_Empenos_Temporal(models.Model):
	empeno_temporal=models.ForeignKey(Empenos_Temporal,on_delete=models.PROTECT)
	kilataje=models.ForeignKey(Kilataje,on_delete=models.PROTECT)
	peso=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)

	class Meta:
		unique_together=('empeno_temporal',)