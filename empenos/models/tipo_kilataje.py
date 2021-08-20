from django.db import models

class Tipo_Kilataje(models.Model):
	tipo_kilataje=models.CharField(max_length=10,null=False)
