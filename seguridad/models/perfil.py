from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Perfil(models.Model):
	perfil=models.CharField(max_length=30,null=False)

	def __str__(self):
		return str(self.id)+' '+self.perfil 