from django.db import models
from empenos.models.abono import Abono
from empenos.models.pagos import Pagos
#no manejamos importe ya que un pago tiene que ser cubierto totalmente, no parcialmente.
#aplica solo para pago semanal
class Rel_Abono_Pago(models.Model):
	abono=models.ForeignKey(Abono,on_delete=models.PROTECT)
	pago=models.ForeignKey(Pagos,on_delete=models.PROTECT)