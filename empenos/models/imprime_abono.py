from django.db import models
from django.contrib.auth.models import User
from empenos.models.abono import Abono

class Imprime_Abono(models.Model):
	usuario=models.ForeignKey(User,on_delete=models.PROTECT)
	abono=models.ForeignKey(Abono,on_delete=models.PROTECT)
	reimpresion=models.IntegerField(default=0)
