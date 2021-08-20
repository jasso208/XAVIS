from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seguridad.models.sucursal import Sucursal
from seguridad.models.perfil import Perfil
from datetime import date, datetime, time,timedelta
from empenos.models import Cajas
from seguridad.models.menu import Menu
from seguridad.models.permisos_usuario import Permisos_Usuario
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
import json
from rest_framework.response import Response

#esta tabla es un complemento de la tabla user de django.
class User_2(models.Model):
	user=models.ForeignKey(User,on_delete=models.PROTECT,related_name = "usuario_sistema")
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT,null=True,blank=True)
	perfil=models.ForeignKey(Perfil,on_delete=models.PROTECT)
	sesion=models.IntegerField(blank=True,null=True)
	usuario_alta = models.ForeignKey(User,on_delete = models.PROTECT,related_name = "usuario_alta_usuario",blank = True,null = True)
	fecha_alta = models.DateTimeField(default = timezone.now())
	usuario_modifica = models.ForeignKey(User,on_delete = models.PROTECT,related_name = "usuario_modifica_usuario",blank = True,null = True)
	fecha_modificacion = models.DateTimeField(default = timezone.now())

	class Meta:
		unique_together=('user',)

	def __str__(self):
		return self.user.username

	def fn_is_logueado(usuario):
		#si no esta logueado mandamos al login
		if not usuario.is_authenticated:
			return None

		#Para que un usuario sea vañido, adebas de estar creado en la tabla User
		#tambien debe tener informacion en la tabla User_2
		try:
			user_2=User_2.objects.get(user=usuario)
		except Exception as e:							
			return None

		return user_2

	#funcion para validar si el usuario tiene caja abierta,
	#en caso de tenerle regresa un objeto de la caja
	#en caso de que no, regresa None
	def fn_tiene_caja_abierta(self):
		try:
			hoy_min = datetime.combine(date.today(),time.min)
			hoy_max = datetime.combine(date.today(),time.max)
			#validamos si el usuaario tiene caja abierta para mostrarla en el encabezado.
			return Cajas.objects.get(fecha__range = (hoy_min,hoy_max),fecha_cierre__isnull = True,usuario = self.user)			
		except Exception as e:
			print(e)
			return None




#*********************************************************************************************
#De aqui para abajo es para la version 2
	###regresa una lista con todos los permsos del usuario
	###se usa para laopcion "administra permisos de usuario"
	###para cargar de inicio los permisos que ya tiene el usuario.
	def fn_consulta_permisos(self):
		resp = []
		permisos = Permisos_Usuario.objects.filter(usuario = self.user)
		for p in permisos:
			resp.append(p.opcion_menu.id)
		return resp

	#api para inciar session
	#parametros 
	#			request
	# 						username
	#						password	
	#Return	
	# 			estatus:	1 exito; 0 error;
	# 			token:		Token para identificar al usuario logueado
	# 			usuario:	Nombre del usuario al que corresponden las credenciales.
	# 			sucursal:	Sucursal a la que pertenece el usuario.			
	def inicia_session(request):
		respuesta = {}
		try:
			username = request.data["username"]
			password = request.data["password"]
		except:
			return {"estatus":"0","msj":"Bad Request."}


		user = authenticate (request,username=username,password=password)

		#si es none, es porque las credenciales son incorectas
		if user == None:
			respuesta = {"estatus":"0","msj":"El usuario y/o contraseña son incorrectos."}

		else:
			try:
				Token.objects.get(user = user).delete()
			except:
				pass

			token = Token.objects.create(user = user)
			user2 = User_2.objects.get(user = user)
			respuesta = {"estatus":"1","token":token.key,"usuario" : user.first_name + ' ' + user.last_name,"sucursal" : user2.sucursal.sucursal}

			#respuesta.append({"usuario" : user.first_name + ' ' + user.last_name})
			#respuesta.append({"sucursal" : user2.sucursal.sucursal})

		return respuesta


	def valida_sesion(token):		
		respuesta = {}
		try:
			usuario = Token.objects.get(key = token).user
			sucursal = User_2.objects.get(user = usuario).sucursal.sucursal
			
			respuesta = {"estatus" : "1","usuario" : usuario.first_name + ' ' + usuario.last_name,"sucursal":sucursal}

		except:			
			respuesta = {"estatus" : "0"}
		return respuesta
