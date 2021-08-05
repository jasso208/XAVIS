from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from empenos.models import Sucursal
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
	sucursal=models.ForeignKey(Sucursal,on_delete=models.PROTECT)
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

	def fn_alta_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,id_usuario_alta):
		resp = []
		if user_name == "" or user_name == None:
			resp.append(False)
			resp.append("El nombre de usuario es requerido.")
			return resp

		try:
			sucursal = Sucursal.objects.get(id = id_sucursal)
		except:
			resp.append(False)
			resp.append("Debe indicar una sucursal valida.")
			return resp

		try:
			Perfil.objects.get(id = id_perfil)
		except:
			resp.append(False)
			resp.append("Debe indicar un perfil valido.")
			return resp


		usuario = User.objects.filter(username = user_name)

		if usuario.exists():
			resp.append(False)
			resp.append("El nombre de usuario indicado ya existe.")
			return resp


		try:
			usuario_alta = User.objects.get(id = int(id_usuario_alta))
			usuario = User()
			usuario.username = user_name
			usuario.first_name = first_name
			usuario.last_name = last_name
			usuario.is_staff = True
			usuario.is_active = True
			usuario.save()

			user_2 = User_2()
			user_2.user = usuario
			user_2.sucursal = Sucursal.objects.get(id = int(id_sucursal))

			user_2.perfil = Perfil.objects.get(id = int(id_perfil))
			user_2.usuario_alta = usuario_alta
			user_2.save()

			resp.append(True)
			resp.append("El usuario se creo correctamente.")
		except Exception as e:
			print(e)
			resp.append(False)
			resp.append("Error al crear el usuario, intente nuevamente.")
			return resp

		return resp


	def fn_edita_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,id_usuario_alta,activo):
		resp = []
		if user_name == "" or user_name == None:
			resp.append(False)
			resp.append("El nombre de usuario es requerido.")
			return resp



		try:
			sucursal = Sucursal.objects.get(id = id_sucursal)
		except:
			resp.append(False)
			resp.append("Debe indicar una sucursal valida.")
			return resp

		try:
			Perfil.objects.get(id = id_perfil)
		except:
			resp.append(False)
			resp.append("Debe indicar un perfil valido.")
			return resp


		try:
			usr_modifica = User.objects.get(id = int(id_usuario_alta))

			usr_a_modificar = User.objects.get(username = user_name)

			u2 = User_2.objects.get(user = usr_a_modificar)

			if u2.fn_tiene_caja_abierta() != None:
				resp.append(False)
				resp.append("El usuario no puede ser modificado ya que cuenta con caja abierta.")
				return resp


			usr_a_modificar.first_name = first_name
			usr_a_modificar.last_name = last_name

			if activo == 0:
				usr_a_modificar.is_active = False
			else:				
				usr_a_modificar.is_active = True

			usr_a_modificar.save()

			user_2 = User_2.objects.get(user = usr_a_modificar)
			user_2.sucursal = Sucursal.objects.get(id = int(id_sucursal))
			user_2.perfil = Perfil.objects.get(id = int(id_perfil))
			user_2.usuario_modifica = usr_modifica
			user_2.fecha_modificacion = timezone.now()

			user_2.save()

			resp.append(True)
			resp.append("El usuario actualizo correctamente.")
		except Exception as e:
			print(e)
			resp.append(False)
			resp.append("Error al actualizar el usuario, intente nuevamente.")
			return resp

		return resp

	def fn_agrega_acceso_a_vista(self,id_menu,id_usuario_asigna):

		resp = []
		if not self.user.is_active:
			resp.append(False)
			resp.append("El usuario esta inactivo, no puede modificar sus permisos.")
			return resp

		try:
			menu = Menu.objects.get( id = id_menu)			
		except Exception as e:			
			print(e)
			resp.append(False)
			resp.append("La opción que intenta agregar no existe o no es valida.")
			return resp

		# Si el usuario ya tiene el permiso asignado, unicamente confirmamos que ya fue asignado
		# para refrescar la pantalla.
		try:
			Permisos_Usuario.objects.get(usuario = self.user,opcion_menu = Menu.objects.get(id = id_menu))			
			resp.append(True)
			resp.append("Se actualizo correctamente.")
			return resp
		except:
			pass



		try:
			pu = Permisos_Usuario()
			pu.usuario = self.user
			pu.opcion_menu = Menu.objects.get(id = id_menu)
			pu.usuario_otorga = User.objects.get(id = id_usuario_asigna)
			pu.save()
		except Exception as e:
			print(e)
			resp.append(False)
			resp.append("Error al actualizar los permisos..")
			return resp


		resp.append(True)
		resp.append("Se actualizo correctamente.")
		return resp

	def fn_remover_acceso_a_vista(self,id_menu):
		resp = []
		if not self.user.is_active:
			resp.append(False)
			resp.append("El usuario esta inactivo, no puede modificar sus permisos.")
			return resp

		#si la opcion que intentamos remover no existe, no importa
		#confirmaoms que ya se removio.
		try:
			menu = Menu.objects.get( id = id_menu)			
		except Exception as e:			
			print(e)
			resp.append(True)
			resp.append("Se actualizo correctamente.")
			return resp

		#removemos el permiso
		Permisos_Usuario.objects.filter(usuario = self.user,opcion_menu = Menu.objects.get(id = id_menu)).delete()

		resp.append(True)
		resp.append("Se actualizo correctamente.")

		return resp

	#regresa true cuando tienepermiso
	#regresa false cuando no tiene permiso
	def fn_tiene_acceso_a_vista(self,id_menu):

		try:
			Permisos_Usuario.objects.get(usuario = self.user,opcion_menu = Menu.objects.get(id = id_menu) )
		except:

			return False		

		return True


	###regresa una lista con todos los permsos del usuario
	###se usa para laopcion "administra permisos de usuario"
	###para cargar de inicio los permisos que ya tiene el usuario.
	def fn_consulta_permisos(self):
		resp = []
		permisos = Permisos_Usuario.objects.filter(usuario = self.user)
		for p in permisos:
			resp.append(p.opcion_menu.id)
		return resp
#*********************************************************************************************
#De aqui para abajo es para la version 2

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