from django.db import models
#esta tabla debera llenarse cada inicio de año para marcar los dias no habiles del año y que la fecha de vencimiento no caiga en estos dias.
class Dia_No_Laboral(models.Model):
    fecha=models.DateTimeField()
    
    class Meta:
        unique_together=("fecha",)
