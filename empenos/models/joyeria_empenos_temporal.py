from django.db import models
from empenos.models.empenos_temporal import Empenos_Temporal
from empenos.models.costo_kilataje import Costo_Kilataje

class Joyeria_Empenos_Temporal(models.Model):
	empeno_temporal=models.ForeignKey(Empenos_Temporal,on_delete=models.PROTECT)
	costo_kilataje=models.ForeignKey(Costo_Kilataje,on_delete=models.PROTECT)
	peso=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)

	class Meta:
		unique_together=('empeno_temporal',)