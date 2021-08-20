from django.db import models

#es la informacion general de la empresa.
#debe haeber sol un registro
class Empresa (models.Model):
	rfc = models.CharField(max_length = 13,default = '')
	nombre_empresa = models.CharField(max_length = 20,default = '')
	horario = models.CharField(max_length = 50,default = '')
