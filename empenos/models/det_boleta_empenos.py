from django.db import models
from empenos.models.costo_kilataje import Costo_Kilataje
from empenos.models.sub_linea import Sub_Linea
from empenos.models.boleta_empeno import Boleta_Empeno
from empenos.models.tipo_producto import Tipo_Producto
from empenos.models.linea import Linea
from empenos.models.marca import Marca

class Det_Boleto_Empeno(models.Model):
	boleta_empeno=models.ForeignKey(Boleta_Empeno,on_delete=models.PROTECT)
	tipo_producto=models.ForeignKey(Tipo_Producto,on_delete=models.PROTECT)
	linea=models.ForeignKey(Linea,on_delete=models.PROTECT)
	sub_linea=models.ForeignKey(Sub_Linea,on_delete=models.PROTECT)	
	marca=models.ForeignKey(Marca,on_delete=models.PROTECT)
	descripcion=models.CharField(max_length=50,null=False)
	costo_kilataje=models.ForeignKey(Costo_Kilataje,on_delete=models.PROTECT,blank=True,null=True)
	peso=models.DecimalField(max_digits=20,decimal_places=2,default=0.00,null=True,blank=True)
	avaluo=models.IntegerField()
	mutuo_sugerido=models.IntegerField()
	mutuo=models.IntegerField()
	observaciones=models.TextField(null=True,blank=True)