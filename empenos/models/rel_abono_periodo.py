from django.db import models
from empenos.models.abono import Abono
from empenos.models.periodo import Periodo
class Rel_Abono_Periodo(models.Model):
	abono=models.ForeignKey(Abono,on_delete=models.PROTECT)
	periodo=models.ForeignKey(Periodo,on_delete=models.PROTECT)	