from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seguridad.models.user_2 import User_2
import json
from rest_framework.authtoken.models import Token
class Login(APIView):

	#para validar si el token corresponde a una session
	#Parametros
	#			token
	#Return
	#			estatus: 1 el token corresponde a usuario; 0 el token no corresponde a usuario
	#			usuario <Opcional>: nombre del usuario al que corresponde el token (solo se regresa en caso de que el token corresponda a un usuario.)
	def get(self,request,format = None):		
		token = request.GET.get("token")
		return Response(json.dumps(User_2.valida_sesion(token)))

	#para iniciar session
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
	def put(self,request,format = None):
		return Response(json.dumps(User_2.inicia_session(request)))	

	#para cerrar session
	#parametros			
	#			request
	#					token	
	def delete(self,request,format = None):		
		try:
			Token.objects.get(key = request.data["token"]).delete()
		except:
			pass
		return Response(json.dumps({"estatus":"1"}))
