from django.db import models

#Solo puede haber un registro 
class Configuracion_Contenido_Impresion(models.Model):
	leyenda_final_venta = models.CharField(max_length = 200,default = '')