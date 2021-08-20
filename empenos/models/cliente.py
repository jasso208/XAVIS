from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

GENERO_CHOICES = (
    ('1','HOMBRE'),
    ('2', 'MUJER'),
)

ESTADO_CIVIL_CHOICES = (
    ('1','SOLTERO'),
    ('2', 'CASADO'),
)



class Cliente(models.Model):
	nombre=models.CharField(max_length = 50,null = False)
	apellido_p=models.CharField(max_length = 50,null = False)
	apellido_m=models.CharField(max_length = 50,default = '',null = True)
	genero=models.CharField(choices=GENERO_CHOICES,max_length=30)
	estado_civil=models.CharField(choices=ESTADO_CIVIL_CHOICES,max_length=30)
	codigo_postal=models.CharField(max_length=10,null=True,default='')
	calle=models.CharField(max_length=50,null=True,default='')
	numero_interior=models.IntegerField(null=True,default=0)
	numero_exterior=models.IntegerField(null=True,default=0)
	colonia=models.CharField(max_length=50,null=True,default='')
	ciudad=models.CharField(max_length=50,null=True,default='')
	estado=models.CharField(max_length=50,null=True,default='')
	pais=models.CharField(max_length=50,null=True,default='')
	telefono_fijo=models.CharField(max_length=10,null=True,default='')
	telefono_celular=models.CharField(max_length=10,null=False)
	usuario=models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True)
	fecha=models.DateTimeField(default=timezone.now)
	nombre_completo = models.CharField (max_length = 100,null = True,blank = True)

	def __str__(self):
		return self.nombre+' '+self.apellido_p+' '+self.apellido_m

	def fn_actualiza_nombre_completo():
		clientes = Cliente.objects.filter(nombre_completo = None) or Cliente.objects.filter(nombre_completo = "")

		for c in clientes:
			apellido_m = ""
			apellido_p = ""
			nombre = ""

			if c.nombre != None:
				nombre = c.nombre.upper()

			if c.apellido_m != None:
				apellido_m = c.apellido_m.upper()

			if c.apellido_p != None:
				apellido_p = c.apellido_p.upper()

			c.nombre_completo = nombre + ' ' +apellido_p + ' ' + apellido_m 
			c.save()
			
	def save(self, *args, **kwargs):
		self.nombre = (self.nombre).upper()
		self.apellido_p = (self.apellido_p).upper()
		self.apellido_m = (self.apellido_m).upper()
		return super(Cliente, self).save(*args, **kwargs)